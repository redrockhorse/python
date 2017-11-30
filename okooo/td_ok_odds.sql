# Host: 127.0.0.1:3318  (Version: 5.6.36)
# Date: 2017-08-13 17:03:57
# Generator: MySQL-Front 5.3  (Build 4.214)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "td_ok_odds"
#

DROP TABLE IF EXISTS `td_ok_odds`;
CREATE TABLE `td_ok_odds` (
  `Id` varchar(50) NOT NULL DEFAULT '' COMMENT 'id',
  `okid` varchar(255) DEFAULT NULL COMMENT '澳客网比赛ID',
  `gametime` datetime DEFAULT NULL COMMENT '比赛时间',
  `provider_id` int(11) DEFAULT NULL COMMENT 'provider_id：99家平均 24,竞彩官方 2，威廉希尔 14，澳门彩票 84，必发 19，立博 82，',
  `w` decimal(10,2) DEFAULT NULL COMMENT '胜赔率',
  `d` decimal(10,2) DEFAULT NULL COMMENT '平赔',
  `l` decimal(10,2) DEFAULT NULL COMMENT '负赔率',
  `t` datetime DEFAULT NULL COMMENT '赔率生产时间',
  `m` varchar(255) DEFAULT NULL COMMENT '赔率生成时间描述',
  `b` varchar(255) DEFAULT NULL COMMENT '未知'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='澳客赔率表';

#
# Data for table "td_ok_odds"
#

