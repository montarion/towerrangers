import hashlib
import json

def setHash(jData):
    jData['hash'] = ''
    sData = bytes(json.dumps(jData, sort_keys=True), 'utf-8')
    m = hashlib.sha256()
    m.update(sData) 
    jData['hash'] = m.hexdigest()
    return jData

def chkHash(jData):
    jData = jData.copy()
    chkHash = jData.get('hash', '')
    jData['hash'] = ''
    sData = bytes(json.dumps(jData, sort_keys=True), 'utf-8')
    m = hashlib.sha256()
    m.update(sData) 
    return chkHash == m.hexdigest()


#
#

if __name__ == '__main__':
    jData1 =  { 'res': 0, 'remark': "Got it"}
    setHash(jData1)
    print(chkHash(jData1), jData1)

    jData2 =  { 'remark': "Got it", 'res': 0 }
    setHash(jData2)
    print(chkHash(jData2), jData2)

    jData2['remark'] = "Changed"
    print(chkHash(jData2), jData2)
