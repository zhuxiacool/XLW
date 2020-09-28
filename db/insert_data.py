from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db.Qrcodemanage

engine = create_engine('mysql+pymysql://root:root@localhost:8887/myPython', pool_recycle=3600)
Session = sessionmaker(bind=engine)  # 使用sessionmaker提供的bind配置定义Session类

session = Session()  # 使用生成的session类创建session 供使用
pr = db.Qrcodemanage.Prizedir()
# 插入奖品类别数据
prize = pr.Prizedir(prizedir_name="和天下",
                    prizedir_code="JP01",
                    prizedir_level="一级")

session.add(prize)
session.commit()