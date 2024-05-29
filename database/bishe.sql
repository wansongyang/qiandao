/*
Navicat MySQL Data Transfer

Source Server         : localhost_3308
Source Server Version : 80012
Source Host           : localhost:3308
Source Database       : django22562xsskqddkxt

Target Server Type    : MYSQL
Target Server Version : 80012
File Encoding         : 65001

Date: 2024-05-28 19:06:44
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `admins`
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL DEFAULT '' COMMENT '帐号',
  `pwd` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员';

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES ('1', 'admin', 'admin');

-- ----------------------------
-- Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(4) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(250) NOT NULL,
  `is_staff` tinyint(4) NOT NULL,
  `is_active` tinyint(4) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `banji`
-- ----------------------------
DROP TABLE IF EXISTS `banji`;
CREATE TABLE `banji` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `banjimingcheng` varchar(255) NOT NULL DEFAULT '' COMMENT '班级名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='班级';

-- ----------------------------
-- Records of banji
-- ----------------------------
INSERT INTO `banji` VALUES ('1', '一班');
INSERT INTO `banji` VALUES ('2', '二班');

-- ----------------------------
-- Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext NOT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(6) NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');
INSERT INTO `django_content_type` VALUES ('7', 'admins', 'admins');
INSERT INTO `django_content_type` VALUES ('8', 'jiaoshi', 'jiaoshi');
INSERT INTO `django_content_type` VALUES ('9', 'xuesheng', 'xuesheng');
INSERT INTO `django_content_type` VALUES ('10', 'banji', 'banji');
INSERT INTO `django_content_type` VALUES ('11', 'qiandaoxinxi', 'qiandaoxinxi');
INSERT INTO `django_content_type` VALUES ('12', 'xueshengqiandao', 'xueshengqiandao');

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('4', 'admin', '0002_logentry_remove_auto_add', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('5', 'admin', '0003_logentry_add_action_flag_choices', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('6', 'contenttypes', '0002_remove_content_type_name', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0002_alter_permission_name_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0003_alter_user_email_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0004_alter_user_username_opts', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0005_alter_user_last_login_null', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('11', 'auth', '0006_require_contenttypes_0002', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('12', 'auth', '0007_alter_validators_add_error_messages', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('13', 'auth', '0008_alter_user_username_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('14', 'auth', '0009_alter_user_last_name_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('15', 'auth', '0010_alter_group_name_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('16', 'auth', '0011_update_proxy_permissions', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('17', 'auth', '0012_alter_user_first_name_max_length', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('18', 'sessions', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('19', 'admins', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('20', 'jiaoshi', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('21', 'xuesheng', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('22', 'banji', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('23', 'qiandaoxinxi', '0001_initial', '2024-05-25 14:07:17');
INSERT INTO `django_migrations` VALUES ('24', 'xueshengqiandao', '0001_initial', '2024-05-25 14:07:17');

-- ----------------------------
-- Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for `jiaoshi`
-- ----------------------------
DROP TABLE IF EXISTS `jiaoshi`;
CREATE TABLE `jiaoshi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gonghao` varchar(50) NOT NULL DEFAULT '' COMMENT '工号',
  `mima` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  `xingming` varchar(50) NOT NULL DEFAULT '' COMMENT '姓名',
  `xingbie` varchar(10) NOT NULL COMMENT '性别',
  `lianxifangshi` varchar(50) NOT NULL DEFAULT '' COMMENT '联系方式',
  `dianziyouxiang` varchar(50) NOT NULL DEFAULT '' COMMENT '电子邮箱',
  `suodaibanji` int(10) unsigned NOT NULL COMMENT '所带班级',
  `jianjie` text NOT NULL COMMENT '简介',
  PRIMARY KEY (`id`),
  KEY `jiaoshi_suodaibanji_index` (`suodaibanji`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='教师';

-- ----------------------------
-- Records of jiaoshi
-- ----------------------------
INSERT INTO `jiaoshi` VALUES ('1', '100', '100', '张老师', '男', '12345678901', '1254@163.com', '1', '11');
INSERT INTO `jiaoshi` VALUES ('2', '200', '200', '陈老师', '男', '12345678902', '552366@qq.com', '2', '11');

-- ----------------------------
-- Table structure for `qiandaoxinxi`
-- ----------------------------
DROP TABLE IF EXISTS `qiandaoxinxi`;
CREATE TABLE `qiandaoxinxi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `qiandaobianhao` varchar(50) NOT NULL DEFAULT '' COMMENT '签到编号',
  `qiandaobanji` int(10) unsigned NOT NULL COMMENT '签到班级',
  `qiandaomingcheng` varchar(255) NOT NULL DEFAULT '' COMMENT '签到名称',
  `qiandaoshijian` varchar(25) NOT NULL COMMENT '签到时间',
  `jiezhishijian` varchar(25) NOT NULL COMMENT '截止时间',
  `shuoming` varchar(255) NOT NULL DEFAULT '' COMMENT '说明',
  `faburen` varchar(64) NOT NULL DEFAULT '' COMMENT '发布人',
  PRIMARY KEY (`id`),
  KEY `qiandaoxinxi_qiandaobanji_index` (`qiandaobanji`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='签到信息';

-- ----------------------------
-- Records of qiandaoxinxi
-- ----------------------------
INSERT INTO `qiandaoxinxi` VALUES ('1', '2405281446861', '1', '课程1', '2024-05-28 14:01:37', '2024-05-28 16:01:37', '111', '100');
INSERT INTO `qiandaoxinxi` VALUES ('2', '2405281870644', '2', '课程a', '2024-05-28 18:04:41', '2024-05-28 19:04:41', '111', '200');

-- ----------------------------
-- Table structure for `xuesheng`
-- ----------------------------
DROP TABLE IF EXISTS `xuesheng`;
CREATE TABLE `xuesheng` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `xuehao` varchar(50) NOT NULL DEFAULT '' COMMENT '学号',
  `mima` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  `xingming` varchar(50) NOT NULL DEFAULT '' COMMENT '姓名',
  `xingbie` varchar(10) NOT NULL COMMENT '性别',
  `lianxidianhua` varchar(50) NOT NULL DEFAULT '' COMMENT '联系电话',
  `suozaibanji` int(10) unsigned NOT NULL COMMENT '所在班级',
  `jianjie` text NOT NULL COMMENT '简介',
  PRIMARY KEY (`id`),
  KEY `xuesheng_suozaibanji_index` (`suozaibanji`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生';

-- ----------------------------
-- Records of xuesheng
-- ----------------------------
INSERT INTO `xuesheng` VALUES ('1', '999', '999', '小明', '男', '13333333333', '1', '11');
INSERT INTO `xuesheng` VALUES ('2', '888', '888', '小陈', '男', '13333344443', '1', '111');
INSERT INTO `xuesheng` VALUES ('3', '777', '777', '小伟', '男', '13334433333', '1', '111');
INSERT INTO `xuesheng` VALUES ('4', '666', '666', '小红', '女', '13333888333', '2', '111');
INSERT INTO `xuesheng` VALUES ('5', '555', '555', '小美', '女', '13333333334', '2', '111');
INSERT INTO `xuesheng` VALUES ('6', '963', '963', '小易', '男', '12345678901', '1', '111');

-- ----------------------------
-- Table structure for `xueshengqiandao`
-- ----------------------------
DROP TABLE IF EXISTS `xueshengqiandao`;
CREATE TABLE `xueshengqiandao` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `qiandaoxinxiid` int(10) unsigned NOT NULL COMMENT '签到信息id',
  `qiandaobianhao` varchar(50) NOT NULL DEFAULT '' COMMENT '签到编号',
  `qiandaobanji` int(10) unsigned NOT NULL COMMENT '签到班级',
  `qiandaomingcheng` varchar(255) NOT NULL DEFAULT '' COMMENT '签到名称',
  `qiandaoshijian` varchar(25) NOT NULL COMMENT '签到时间',
  `jiezhishijian` varchar(25) NOT NULL COMMENT '截止时间',
  `xueshengqiandaoshijian` varchar(50) NOT NULL DEFAULT '' COMMENT '学生签到时间',
  `didian` varchar(50) NOT NULL DEFAULT '' COMMENT '地点',
  `beizhu` text NOT NULL COMMENT '备注',
  `xueshengxingming` varchar(50) NOT NULL DEFAULT '' COMMENT '学生姓名',
  `xueshengxuehao` varchar(64) NOT NULL DEFAULT '' COMMENT '学生学号',
  `shifouchidao` varchar(50) NOT NULL COMMENT '是否迟到',
  `faburen` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布人',
  PRIMARY KEY (`id`),
  KEY `xueshengqiandao_qiandaoxinxiid_index` (`qiandaoxinxiid`),
  KEY `xueshengqiandao_qiandaobanji_index` (`qiandaobanji`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生签到';

-- ----------------------------
-- Records of xueshengqiandao
-- ----------------------------
INSERT INTO `xueshengqiandao` VALUES ('1', '1', '2405281446861', '1', '课程1', '2024-05-28 14:01:37', '2024-05-28 16:01:37', '2024-05-28 14:09:19', 'XXXX', '11', '小明', '999', '未迟到', '100');
INSERT INTO `xueshengqiandao` VALUES ('2', '1', '2405281446861', '1', '课程1', '2024-05-28 14:01:37', '2024-05-28 16:01:37', '2024-05-28 14:10:01', 'XXXX', '11', '小陈', '888', '未迟到', '100');
INSERT INTO `xueshengqiandao` VALUES ('3', '1', '2405281446861', '1', '课程1', '2024-05-28 14:01:37', '2024-05-28 16:01:37', '2024-05-28 17:10:20', 'XXXX', '11', '小伟', '777', '迟到', '100');
INSERT INTO `xueshengqiandao` VALUES ('4', '2', '2405281870644', '2', '课程a', '2024-05-28 18:04:41', '2024-05-28 19:04:41', '2024-05-28 18:05:05', 'XXXX', '111', '小红', '666', '未迟到', '200');
INSERT INTO `xueshengqiandao` VALUES ('5', '2', '2405281870644', '2', '课程a', '2024-05-28 18:04:41', '2024-05-28 19:04:41', '2024-05-28 19:05:29', 'XXXX', '11', '小美', '555', '迟到', '200');
