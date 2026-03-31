"""Genera certificado SSL autofirmado para desarrollo"""
import ssl
import datetime
import os

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

def generate_with_cryptography():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"TotemIA Dev"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                x509.IPAddress(ipaddress.IPv4Address("10.10.48.33")),
                x509.IPAddress(ipaddress.IPv4Address("0.0.0.0")),
            ]), critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    print("Certificado generado con cryptography")

def generate_with_ssl():
    """Fallback: usa subprocess con certutil o genera con ssl stdlib"""
    # Generar con un one-liner de Python puro usando ssl
    import subprocess
    import tempfile
    # Intentar con PowerShell New-SelfSignedCertificate + export
    # Más simple: generar con Python ssl module no es posible directamente
    # Usamos un approach diferente: script de servidor con ssl wrapping
    print("NO_CERT")

if __name__ == "__main__":
    import ipaddress
    if HAS_CRYPTO:
        generate_with_cryptography()
    else:
        generate_with_ssl()
