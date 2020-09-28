from sqlalchemy import (Table, Column, Integer, Numeric, String, Boolean, BigInteger,
                        DateTime, insert, update, delete, select, create_engine, ForeignKey, BigInteger, Text, null)
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound

engine = create_engine('mysql+pymysql://root:root@localhost:8887/myPython', echo=True, pool_recycle=3600)
Session = sessionmaker(bind=engine)  # 使用sessionmaker提供的bind配置定义Session类

session = Session()  # 使用生成的session类创建session 供使用

Base = declarative_base()


# 奖品目录表
class Prizedir(Base):
    __tablename__ = 'prizedir'

    prizedir_id = Column(Integer(), primary_key=True)
    prizedir_name = Column(String(50), nullable=False, comment="奖品目录名称")
    prizedir_code = Column(String(20), nullable=False, comment="分类代码")
    prizedir_level = Column(String(50), default="未设置", comment="奖品级别")

    def __repr__(self):
        return "Prizedir(prizedir_id ={self.prizedir_id}, " \
               "prizedir_name = '{self.prizedir_name}', " \
               "prizedir_code = '{self.prizedir_code}', " \
               "prizedir_level = '{self.prizedir_level}')".format(self=self)




# 奖品编码记录表  （id，编码，目录id，状态，入库，操作人，出库，操作人，上机，操作人，机器id,出奖，C日期，U日期）
class Prize(Base):
    __tablename__ = "prize"

    prize_id = Column(BigInteger(), primary_key=True)
    prize_code = Column(String(255), nullable=False, unique=True, index=True, comment="奖品编码")
    prizedir_id = Column(Integer(), ForeignKey('prizedir.prizedir_id'))
    prize_state = Column(String(20), default="入库", comment="状态")
    prize_warehouse_in = Column(Boolean(), default=0, comment="是否入库")
    operator_in = Column(Integer(), ForeignKey('users.users_id'), comment="入库操作人")
    in_time = Column(DateTime(), default=datetime.now(), comment="入库操作发生时间")
    prize_warehouse_out = Column(Boolean(), default=0, comment="是否出库")
    operator_out = Column(Integer(), ForeignKey('users.users_id'), comment="出库操作人")
    out_time = Column(DateTime(), default=datetime.now(), comment="出库操作发生时间")
    salesman = Column(Integer(), ForeignKey('users.users_id'), default=null, comment="业务负责")
    prize_machine_in = Column(Boolean, default=0, comment="是否上机")
    machine_in = Column(Integer(), ForeignKey('users.users_id'), default=null, comment="上机操作人")
    machine_in_time = Column(DateTime(), comment="上机操作发生时间")
    machine_id = Column(Integer(), ForeignKey('machine.machine_id'), default=null, comment="机器ID")
    prize_machine_out = Column(Boolean, default=0, comment="是否出奖")
    machine_out_time = Column(DateTime(), comment="出奖操作发生时间")
    machine_out_qrcode = Column(Integer(), ForeignKey('qrcodescan.qrcode_id'), comment='出奖奖票二维码')
    machine_isdone = Column(Boolean(), default=0, comment="奖品是否已出")
    created_on = Column(DateTime(), default=datetime.now(), comment="记录创建时间")
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后更新时间")
    # prizedir = relationship("Prizedir", backref(backref('prizedir', order_by=id)))
    # w_in_user = relationship('Users', backref(backref('users', order_by=id)))
    # w_out_user = relationship('Users', backref(backref('users', order_by=id)))
    # w_salesman = relationship('Users', backref(backref('users', order_by=id)))
    # m_up = relationship('Users', backref(backref('users', order_by=id)))
    # m_up_user = relationship('Users', backref(backref('users', order_by=id)))
    # m_sn = relationship('Machine', backref(backref('machine', order_by=id)))
    m_down_code = relationship('QrcodeScan', backref(backref('qrcodescan', order_by=id)))

    def __repr__(self):
        return "prize(prize_id = {self.prize_id}. " \
               "prize_code = '{self.prize_code}'," \
               "prizedir = '{self.prizedir}', " \
               "prize_warehouse_in = {self.prize_warehouse_in}, " \
               "w_in_user = '{self.w_in_user}', " \
               "in_time = '{self.in_time}', " \
               "prize_warehouse_out = {self.prize_warehouse_out}, " \
               "w_out_user = '{self.w_out_user}', " \
               "w_salesman = '{self.w_salesman}'," \
               "out_time = '{self.out_time}', " \
               "prize_machine_in = {self.prize_machine_in}, " \
               "m_up = '{self.m_up}'," \
               "machine_in_time = '{self.machine_in_time}', " \
               "prize_machine_out = {self.prize_machine_out}, " \
               "m_up_user = '{self.m_up_user}', " \
               "m_sn = '{self.m_sn}', " \
               "m_down_code = '{self.m_down_code}'" \
               "machine_out_time = '{self.machine_out_time}', " \
               "created_on = '{self.created_on}', " \
               "updated_on = '{self.updated_on}')".format(self=self)

prize1 = Prize(prize_code="jp01000000000000",
               prizedir_id=1,
               prize_state="入库",
               prize_warehouse_in=True,
               operator_in=1
               )

prize2 = Prize(prize_code="jp02000000000000",
               prizedir_id=2,
               prize_state="入库",
               prize_warehouse_in=True,
               operator_in=1
               )

prize3 = Prize(prize_code="jp03000000000000",
               prizedir_id=3,
               prize_state="入库",
               prize_warehouse_in=True,
               operator_in=1
               )


#               )
# session.add(prize)
# session.commit()
# #
#
#
#
#
# # 机器库存表（id, 机器ID，奖品目录，库存上限，库存量，)
# class Machinehouse(Base):
#     __tablename__ = "machine_house"
#
#     machinehouse_id = Column(Integer(), primary_key=True)
#     machine_id = Column(Integer(), ForeignKey('machine.machine_id'), comment="机器ID")
#     prize_dir_id = Column(Integer(), ForeignKey('prizedir.prizedir_id'), comment="目录ID")
#     max_stock = Column(Integer(), default=10, comment="库存上限")
#     now_stock = Column(Integer(), default=0, comment="现在库存")
#     created_on = Column(DateTime(), default=datetime.now())
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#
#     machine = relationship('Machine', backref(backref('machine', orderby=id)))
#     prizedir = relationship("Prizedir", backref(backref('prizedir', order_by=id)))
#
#     def __repr__(self):
#         return "Machinehouse(machinehouse_id = {self.machinehouse_id}, " \
#                "max_stock = '{self.max_stock}', " \
#                "now_stock = '{self.now_stock}', " \
#                "machine = '{self.machine}', " \
#                "prizedir = '{self.prizedir}', " \
#                "created_on = '{self.created_on}', " \
#                "updated_on = '{self.updated_on}')".format(self=self)
#
#
# 用户表（用户名，电话，邮件，密码，头像，账号激活）
class Users(Base):
    __tablename__ = "users"

    users_id = Column(Integer(), primary_key=True)
    user_name = Column(String(20), nullable=False, comment="用户名")
    phone = Column(String(20), nullable=False, comment="电话号码")
    email_address = Column(String(50), comment="邮件地址")
    password = Column(String(20), nullable=False, comment="密码")
    avatar = Column(String(255), comment="头像地址")
    actioned = Column(Boolean(), default=False, comment="账号激活")

    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "Users(users_id = {self.users_id}, " \
               "user_name = '{self.user_name}', " \
               "user_phone = '{self.phone}', " \
               "email_address = '{self.email_address}', " \
               "password = '{self.password}', " \
               "avatar = '{self.avatar}', " \
               "actioned = '{self.actioned}', " \
               "created_on = '{self.created_on}', " \
               "updated_on = '{self.updated_on}')".format(self=self)


#
#
# 机器表（序列号，SIM卡，机器类型，激活状态，激活时间，工作状态，位置，中奖模式，IP地址，生产时间
class Machine(Base):
    __tablename__ = "machine"

    machine_id = Column(Integer(), primary_key=True)
    machine_sn = Column(String(100), nullable=False, unique=True, comment="序列号")
    machine_sim = Column(String(20), comment="sim卡号")
    machine_type_id = Column(Integer(), ForeignKey('machine_type.type_id'), comment="机器类型")
    machine_actioned = Column(Boolean(), default=0, comment="激活状态")
    actioned_time = Column(DateTime(), comment="激活时间")
    actioned_user = Column(Integer(), ForeignKey('users.users_id'))
    machine_workstate = Column(Integer(), ForeignKey('machine_workstate.workstate_id'))
    machine_point = Column(String(255), comment="机器位置")
    gamemode_id = Column(Integer(), ForeignKey('game_mode.game_mode_id'), comment="中奖模式")
    ipaddress = Column(String(40), comment="IP地址")
    made_time = Column(DateTime(), comment="生产时间")
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    ac_user = relationship('Users', backref=backref('machine', order_by=machine_id))
   # manage = relationship('Users', backref=backref('machine', order_by=machine_id))
   # type = relationship('MachineType', backref=backref('machine', order_by=machine_id))
   # workstate = relationship('Game_Mode', backref=backref('machine', order_by=machine_id))

    def __repr__(self):
        return "Machine(machine_id = {self.machine_id}, " \
               "machine_sn = '{self.machine_sn}', " \
               "machine_sim = '{self.machine_sim}', " \
               "type = '{self.type}', " \
               "machine_actioned = {self.machine_actioned}, " \
               "ac_user = '{self.ac_user}', " \
               "actioned_time = '{self.actioned_time}', " \
               "manage = '{self.manage}'," \
               "workstate = '{self.workstate}', " \
               "machine_point = '{self.machine_point}', " \
               "ipaddress = '{self.ipaddress}', " \
               "created_on = '{self.created_on}', " \
               "updated_on = '{self.updated_on}')".format(self=self)




# 中奖模式（类型名称，总数，n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,normal)
class GameMode(Base):
    __tablename__ = "game_mode"

    game_mode_id = Column(Integer(), primary_key=True)
    gamemode_name = Column(String(50), nullable=False, comment="名称")
    gamemode_count = Column(Integer(), default=0, comment="中奖周期总数")
    gamemode_n1 = Column(Integer(), default=0, comment="奖项一")
    gamemode_n2 = Column(Integer(), default=0, comment="奖项二")
    gamemode_n3 = Column(Integer(), default=0, comment="奖项三")
    gamemode_n4 = Column(Integer(), default=0, comment="奖项四")
    gamemode_n5 = Column(Integer(), default=0, comment="奖项五")
    gamemode_n6 = Column(Integer(), default=0, comment="奖项六")
    gamemode_n7 = Column(Integer(), default=0, comment="奖项七")
    gamemode_n8 = Column(Integer(), default=0, comment="奖项八")
    gamemode_n9 = Column(Integer(), default=0, comment="奖项九")
    gamemode_n10 = Column(Integer(), default=0, comment="奖项十")
    gamemode_normal = Column(Integer(), default=0, comment="无奖")
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "GameMode(gamemode_name = '{self.gamemode_name}', " \
               "gamemode_n1 = {self.gamemode_n1}" \
               "gamemode_n2 = {self.gamemode_n2}" \
               "gamemode_n3 = {self.gamemode_n3}" \
               "gamemode_n4 = {self.gamemode_n4}" \
               "gamemode_n5 = {self.gamemode_n5}" \
               "gamemode_normal = {self.gamemode_normal}" \
               "created_on = '{self.created_on}', " \
               "updated_on = '{self.updated_on}')".format(self=self)



# 机器GPS位置存储与表示
# class MachinePoint(Base):
#     __tablename__ = "point"
#
#     point_id = Column(Integer(), primary_key=True)
#     point_L = Column(Numeric, default=0.00, comment="经度")
#     point_B = Column(Numeric, default=0.00, comment="纬度")
#     point_address = Column(String(255), comment="经纬度转换地址")
#     machine_id = Column(Integer(), ForeignKey('machine.machine_id'), comment="机器ID")
#     created_on = Column(DateTime(), default=datetime.now())
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#
#     machine = relationship('Machine', backref(backref('machine', orderby=id)))
#
#     def __repr__(self):
#         return "MachinePoint(point_L = {self.point_L}), " \
#                "point_B = {self.point_R}, " \
#                "machine = '{self.machine}', " \
#                "point_address = '{self.point_address}', " \
#                "created_on = '{self.created_on}', " \
#                "updated_on = '{self.updated_on}')".format(self=self)

# 机器的类型
class MachineType(Base):
    __tablename__ = "machine_type"

    type_id = Column(Integer(), primary_key=True)
    type_name = Column(String(50), nullable=False, comment="机器类型名称")

    def __repr__(self):
        return "MachineType(typename = '{self.type_name} )".format(self=self)





# 机器的状态
class WorkState(Base):
    __tablename__ = "machine_workstate"

    workstate_id = Column(Integer(), primary_key=True)
    workstate_name = Column(String(20), nullable=False, comment="工作状态")

    def __repr__(self):
        return "WorkState(workstate_name = '{self.workstate_name}')".format(self=self)




# 机器扫描的二维码和二维码状态、处理日志等
class QrcodeScn(Base):
    __tablename__ = "qrcodescan"
    qrcode_id = Column(Integer(), primary_key=True)
    machine_id = Column(Integer(), ForeignKey('machine.machine_id'), comment="获得二维码的机器ID")
    qrcode = Column(String(255), nullable=False, index=True, comment="机器扫描二维码")
    code_check = Column(Boolean(), nullable=False, comment="是否有效")
    Nnum = Column(String(20), comment="抽奖结果")
    log = Column(Text(), comment="系统日志")
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    machine = relationship('Machine', backref(backref('machine', orderby=id)))


# 创建表

Base.metadata.create_all(engine)

"""
必须先插入基础数据，才能对有外键的表操作
"""
# 插入机器状态数据
wordstate1 = WorkState(workstate_name="在线")
wordstate2 = WorkState(workstate_name="离线")
wordstate3 = WorkState(workstate_name="无数据更新")
session.add(wordstate1)
session.add(wordstate2)
session.add(wordstate3)
session.commit()

# 插入用户数据
user1 = Users(user_name="管理员",
              phone="18684864559",
              email_address="451993762@qq.com",
              password="password",
              avatar="",
              actioned=True,
              )
user2 = Users(user_name="唐丽",
              phone="18684864558",
              email_address="18684864558@qq.com",
              password="password",
              avatar=""
              )
user3 = Users(user_name="朱侠",
              phone="18684864559",
              email_address="18684864558@qq.com",
              password="password",
              avatar="")
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()


# 插入机器类型数据
type1 = MachineType(type_name="台式A型")
type2 = MachineType(type_name="台式B型")
type3 = MachineType(type_name="台式C型")
type4 = MachineType(type_name="立式A型")
type5 = MachineType(type_name="立式B型")
type6 = MachineType(type_name="立式C型")
session.add(type1)
session.add(type2)
session.add(type3)
session.add(type4)
session.add(type5)
session.add(type6)
session.commit()

#插入中奖模式数据
gamemode = GameMode(gamemode_name='十中七',
                    gamemode_n1=1,
                    gamemode_n2=2,
                    gamemode_n3=2,
                    gamemode_n4=3,
                    gamemode_normal=2,
                    gamemode_count=10)
session.add(gamemode)
session.commit()

# 插入奖品目录数据

prize1 = Prizedir(prizedir_name="和天下",
                  prizedir_code="JP01",
                  prizedir_level="一级")

prize2 = Prizedir(prizedir_name="芙蓉王",
                  prizedir_code="JP02",
                  prizedir_level="二级")

prize3 = Prizedir(prizedir_name="清风纸巾",
                  prizedir_code="JP03",
                  prizedir_level="三级")

prize4 = Prizedir(prizedir_name="神秘红包",
                  prizedir_code="JP04",
                  prizedir_level="四级")

# 插入数据
session.add(prize1)
session.add(prize2)
session.add(prize3)
session.add(prize4)
session.commit()
print(prize1)
print(prize2)
print(prize3)
print(prize4)


"""
带外键的表操作
"""


#插入机器数据

machine = Machine(machine_sn="XLW0000002",
                  machine_sim="123456789",
                  machine_type_id=1,
                  actioned_user=1,
                  machine_workstate=1,
                  gamemode_id=1,
                  ipaddress="192.168.123.228",
                  )
session.add(machine)

try:
    session.commit()
except MultipleResultsFound as error:
    print(MultipleResultsFound)