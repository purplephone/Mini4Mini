import configparser, os, certifi

env = configparser.ConfigParser()
env.read(os.getcwd() + os.sep + 'config.ini', encoding='utf-8')

SECRET_KEY = env['SECRET_KEY']['KEY']
DB_LINK = env['DB_LINK']['LINK']
CA = certifi.where()

if __name__ == '__main__':
    print(SECRET_KEY)
    print(DB_LINK)
    print(CA)