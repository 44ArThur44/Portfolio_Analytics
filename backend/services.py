import os
import hashlib
from typing import Optional
try:
    import geoip2.database as geoip2
except Exception:
    geoip2 = None

GEOIP_DB = os.getenv('GEOIP_DB')
IP_SALT = os.getenv('VISIT_SALT', 'change-me')

def anonymize_ip(ip: Optional[str]) -> str:
    if not ip:
        return '0'
    h = hashlib.sha256()
    h.update(IP_SALT.encode('utf-8'))
    h.update(ip.encode('utf-8'))
    return h.hexdigest()

def lookup_country(ip: Optional[str]) -> str:
    if not ip:
        return 'ZZ'
    if GEOIP_DB and geoip2:
        try:
            reader = geoip2.database.Reader(GEOIP_DB)
            rec = reader.country(ip)
            country = (rec.country.iso_code or 'ZZ')
            reader.close()
            return country
        except Exception:
            return 'ZZ'
    return 'ZZ'
