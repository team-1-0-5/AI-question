/*
 Navicat Premium Dump SQL

 Source Server         : summer
 Source Server Type    : MySQL
 Source Server Version : 80037 (8.0.37)
 Source Host           : localhost:3306
 Source Schema         : ai_question

 Target Server Type    : MySQL
 Target Server Version : 80037 (8.0.37)
 File Encoding         : 65001

 Date: 23/07/2025 17:05:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for allocation
-- ----------------------------
DROP TABLE IF EXISTS `allocation`;
CREATE TABLE `allocation`  (
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  `times` datetime NOT NULL,
  PRIMARY KEY (`user_id`, `question_id`, `times`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of allocation
-- ----------------------------

-- ----------------------------
-- Table structure for create_speech
-- ----------------------------
DROP TABLE IF EXISTS `create_speech`;
CREATE TABLE `create_speech`  (
  `speech_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of create_speech
-- ----------------------------
INSERT INTO `create_speech` VALUES (8, 1);
INSERT INTO `create_speech` VALUES (9, 1);

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS `file`;
CREATE TABLE `file`  (
  `file_id` int NOT NULL AUTO_INCREMENT,
  `file_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`file_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of file
-- ----------------------------
INSERT INTO `file` VALUES (17, 'uploads\\123123_1.txt_1752671980.4293556', 'courseware');
INSERT INTO `file` VALUES (18, 'uploads\\1__1753183088.8613737_121.txt', 'courseware');

-- ----------------------------
-- Table structure for join_speech
-- ----------------------------
DROP TABLE IF EXISTS `join_speech`;
CREATE TABLE `join_speech`  (
  `user_id` int NOT NULL,
  `speech_id` int NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of join_speech
-- ----------------------------
INSERT INTO `join_speech` VALUES (2, 9);

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question`  (
  `question_id` int NOT NULL,
  `options` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `answer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`question_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of question
-- ----------------------------

-- ----------------------------
-- Table structure for question_user
-- ----------------------------
DROP TABLE IF EXISTS `question_user`;
CREATE TABLE `question_user`  (
  `question_id` int NOT NULL,
  `user_id` int NOT NULL,
  `user_answer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`question_id` DESC, `user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of question_user
-- ----------------------------

-- ----------------------------
-- Table structure for speech
-- ----------------------------
DROP TABLE IF EXISTS `speech`;
CREATE TABLE `speech`  (
  `speech_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `begin_time` datetime NOT NULL,
  `state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`speech_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech
-- ----------------------------
INSERT INTO `speech` VALUES (2, '一个演讲', '简介', '2022-05-25 20:00:00', '');
INSERT INTO `speech` VALUES (3, '一个演讲', '简介', '2022-05-25 20:00:00', '');
INSERT INTO `speech` VALUES (4, '一个演讲', '简介', '2022-05-25 20:00:00', '');
INSERT INTO `speech` VALUES (5, '一个演讲', '简介', '2022-05-25 20:00:00', '');
INSERT INTO `speech` VALUES (7, '演讲创建测试', NULL, '2025-07-22 19:40:16', '');
INSERT INTO `speech` VALUES (8, '演讲创建测试', NULL, '2025-07-22 19:40:42', '');
INSERT INTO `speech` VALUES (9, '演讲创建测试', NULL, '2025-07-22 19:42:12', '');

-- ----------------------------
-- Table structure for speech_file
-- ----------------------------
DROP TABLE IF EXISTS `speech_file`;
CREATE TABLE `speech_file`  (
  `speech_id` int NOT NULL,
  `file_id` int NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech_file
-- ----------------------------
INSERT INTO `speech_file` VALUES (8, 17);
INSERT INTO `speech_file` VALUES (9, 17);
INSERT INTO `speech_file` VALUES (9, 18);

-- ----------------------------
-- Table structure for speech_question
-- ----------------------------
DROP TABLE IF EXISTS `speech_question`;
CREATE TABLE `speech_question`  (
  `speech_id` int NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`question_id` DESC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech_question
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_type` int NOT NULL COMMENT '0听众，1演讲者',
  PRIMARY KEY (`user_id` DESC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (2, '123456', 'test', 0);
INSERT INTO `user` VALUES (1, '1231', 'hhh', 1);

-- ----------------------------
-- Table structure for user_file
-- ----------------------------
DROP TABLE IF EXISTS `user_file`;
CREATE TABLE `user_file`  (
  `user_id` int NOT NULL,
  `file_id` int NOT NULL,
  PRIMARY KEY (`file_id`, `user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_file
-- ----------------------------
INSERT INTO `user_file` VALUES (123123, 17);
INSERT INTO `user_file` VALUES (1, 18);

SET FOREIGN_KEY_CHECKS = 1;
