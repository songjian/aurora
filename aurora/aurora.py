import psutil,os,requests,json,tempfile
import pandas as pd

class AuroraVPN():

    def __init__(self, vpn_app_name:str='aurora.exe'):
        aurora_release_path =  os.path.join(tempfile.gettempdirb(), b'Aurora-release')
        with open(aurora_release_path, 'r') as f:
            aurora_release = f.read()
        self.release = aurora_release[0:-7]
        self.vpn_app_name = vpn_app_name
    
    def get_lines(self):
        """
        得到线路
        """
        url = self.release + 'lines'
        r = requests.get(url)
        str = json.loads(r.text)
        df = pd.DataFrame(str.get('data').get('lines'))
        return df
    
    def connect(self):
        """
        连接
        """
        url = self.release + 'client/connect'
        r = requests.get(url)
        return r.text
    
    def disconnect(self):
        """
        断开连接
        """
        url = self.release + 'client/disconnect'
        r = requests.get(url)
        return r.text

    def switch(self, guid:str=None):
        """
        切换线路
        """
        if guid is None:
            line = self.random_line(rank=4, location='hk,jp,cn')
            guid = line.iloc[0, 0]
        
        url = self.release + 'line/connect'
        data = json.dumps({'guid': guid})
        r = requests.post(url, data=data)
        j = json.loads(r.text)
        return True if j.get('code') == 0 else False
    
    def random_line(self, rank:int=4, location:str='hk,jp,cn'):
        """随机选取线路

        Args:
            rank: 线路质量排名，一般选择大于4的
            location: 线路地区简码，多个使用英文逗号分隔，例: hk,jp,cn
        
        Returns:
            返回线路的pandas DataFrame对象
        """
        location_list = location.split(',')
        lines = self.get_lines()
        return lines[(lines['connected'] == False) & (lines['is_vip'] == True) & (lines['rank'] >= rank) & (lines['location'].isin(location_list))].sample(1)

    def isconnect(self):
        """
        检查VPN连接
        """
        lines = self.get_lines()
        return False if lines[lines['connected'] == True].empty else True

    def is_running(self):
        for proc in psutil.process_iter(['pid', 'name']):
            # print(proc.info)
            if proc.info.get('name') == self.vpn_app_name:
                return True
        return False
        

if __name__ == '__main__':
    v = AuroraVPN()
    print(v.switch())