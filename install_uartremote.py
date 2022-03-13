import ubinascii, uos, machine,uhashlib
from ubinascii import hexlify
b64="""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
"""

def calc_hash(b):
    return hexlify(uhashlib.sha256(b).digest()).decode()

# this is the hash of the compiled uartremote.mpy
hash_gen='13cab9bff9ce7c1eb4639c5807b14c98ea0c228a6f4e1284d6ae127ead603fac'

uartremote=ubinascii.a2b_base64(b64)
hash_initial=calc_hash(uartremote)

with open('/projects/uartremote.mpy','wb') as f:
    f.write(uartremote)
uartremote_check=open('/projects/uartremote.mpy','rb').read()
hash_check=calc_hash(uartremote_check)

error=False
if hash_initial != hash_gen:
    error=True
if hash_check != hash_gen:
    error=True

if not error:
    print('Uartremote library written succesfully')
else:
    print('Failure in Uartremote library!')