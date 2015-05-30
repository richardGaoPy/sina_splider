import re
import json
str = 'sinaSSOController.preloginCallBack({"retcode":0,"servertime":1432889506,"pcid":"xd-5d282fab4ec837a55380af4c0dc73f211d39","nonce":"MQJDK9","pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","showpin":1,"exectime":9})'

def test():
     p = re.compile('preloginCallBack(.+)')
     data = p.search(str).group(1)
     data = json.loads(data[1:-1])
     print data
     from PIL import Image
     Image.open('pin.png')

if __name__ == "__main__":
    test()