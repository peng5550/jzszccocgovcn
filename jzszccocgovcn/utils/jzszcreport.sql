/*
Navicat MySQL Data Transfer

Source Server         : peng
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : project

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2020-10-11 20:07:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jzszcreport
-- ----------------------------
DROP TABLE IF EXISTS `jzszcreport`;
CREATE TABLE `jzszcreport` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `gender` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `nation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `idType` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `idNo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `school` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `major` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `education` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `degree` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `graduation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyNameNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyNatureNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyRegistrationPlaceNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyLegalPersonNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyTypeNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `postNoNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `addressNow` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyNameBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyNatureBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyRegistrationPlaceBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyLegalPersonBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `companyTypeBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `postNoBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `addressBefore` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `startDate` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `endDate` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `headImage` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `signImage` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `idCardImage` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `registerFlowId` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of jzszcreport
-- ----------------------------
INSERT INTO `jzszcreport` VALUES ('1', '林明福', '男', '01', '307371210@qq.com', '1', '350823198609091657', '15080287837', '福建工程学院', '土木工程', '5', '5', '2009-6-19 ', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2016-01-01', '2019-12-31', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=1', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=12&random=0.32922125', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=2, http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=3, http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=4', 'http://jzszc.coc.gov.cn/jsbZcgl/client/registrationReview/censor/goreport.htm?registerFlowId=1&processtypecode=02&sbzt=1&registerId=&examsCode%20=');
INSERT INTO `jzszcreport` VALUES ('2', '张曦', '男', '01', '2633833570@qq.com', '1', '62010319770424265X', '13909481725', '兰州工业高等专科学校', '房屋建筑工程', '4', '99', '2000-6-28 ', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2017-05-17', '2017-05-17', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=81578B0315F921A430CD553F00AD8867&pictype=1', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=81578B0315F921A430CD553F00AD8867&pictype=12&random=0.8815153', 'http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=81578B0315F921A430CD553F00AD8867&pictype=2, http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=81578B0315F921A430CD553F00AD8867&pictype=3, http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=81578B0315F921A430CD553F00AD8867&pictype=4', 'http://jzszc.coc.gov.cn/jsbZcgl/client/registrationReview/censor/goreport.htm?registerFlowId=2&processtypecode=02&sbzt=1&registerId=&examsCode%20=');
