# Host: 127.0.0.1:3318  (Version: 5.6.36)
# Date: 2017-08-12 10:13:34
# Generator: MySQL-Front 5.3  (Build 4.214)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "td_ok_gamebaseinfo"
#

DROP TABLE IF EXISTS `td_ok_gamebaseinfo`;
CREATE TABLE `td_ok_gamebaseinfo` (
  `Id` varchar(50) NOT NULL DEFAULT '0' COMMENT '主键，年月日+竞彩的比赛ID',
  `okid` varchar(100) DEFAULT NULL COMMENT '澳客网赛事ID，用于查找详情页面',
  `gametime` datetime DEFAULT NULL COMMENT '比赛时间',
  `lg` varchar(255) DEFAULT NULL COMMENT '比赛类别',
  `hmname` varchar(255) DEFAULT NULL COMMENT '主队名称',
  `ayname` varchar(255) DEFAULT NULL COMMENT '客队名称',
  `season` varchar(255) DEFAULT NULL COMMENT '赛季',
  `gamerule` varchar(255) DEFAULT NULL COMMENT '赛制',
  `round` varchar(255) DEFAULT NULL COMMENT '轮次',
  `field` varchar(255) DEFAULT NULL COMMENT '比赛场地',
  `weather` varchar(255) DEFAULT NULL COMMENT '天气',
  `temperature` varchar(255) DEFAULT NULL COMMENT '温度',
  `h_t_w` int(11) DEFAULT NULL COMMENT '主队总胜场次',
  `h_t_d` int(11) DEFAULT NULL COMMENT '主队总平场次',
  `h_t_l` int(11) DEFAULT NULL COMMENT '主队总负场次',
  `h_t_s` int(11) DEFAULT NULL COMMENT '主队总积分',
  `h_t_o` int(11) DEFAULT NULL COMMENT '主队总排名',
  `h_h_w` int(11) DEFAULT NULL COMMENT '主队主场胜场次',
  `h_h_d` int(11) DEFAULT NULL COMMENT '主队主场平场次',
  `h_h_l` int(11) DEFAULT NULL COMMENT '主队主场负场次',
  `h_h_s` int(11) DEFAULT NULL COMMENT '主队主场积分',
  `h_h_o` int(11) DEFAULT NULL COMMENT '主队主场排名',
  `a_t_w` int(11) DEFAULT NULL COMMENT '客队总胜场次',
  `a_t_d` int(11) DEFAULT NULL COMMENT '客队总平场次',
  `a_t_l` int(11) DEFAULT NULL COMMENT '客队总负场次',
  `a_t_s` int(11) DEFAULT NULL COMMENT '客队总积分',
  `a_t_o` int(11) DEFAULT NULL COMMENT '客队总排名',
  `a_a_w` int(11) DEFAULT NULL COMMENT '客队客场胜场次',
  `a_a_d` int(11) DEFAULT NULL COMMENT '客队客场平场次',
  `a_a_l` int(11) DEFAULT NULL COMMENT '客队客场负场次',
  `a_a_s` int(11) DEFAULT NULL COMMENT '客队客场积分',
  `a_a_o` int(11) DEFAULT NULL COMMENT '客队客场排名',
  `hscore` int(11) DEFAULT NULL COMMENT '主队进球数',
  `ascore` int(11) DEFAULT NULL COMMENT '客队进球数',
  `h_hs` int(11) DEFAULT NULL COMMENT '半场主队进球数',
  `h_as` int(11) DEFAULT NULL COMMENT '半场客队进球数',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='澳客网比赛基础信息表';

#
# Data for table "td_ok_gamebaseinfo"
#

