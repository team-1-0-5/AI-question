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

 Date: 16/07/2025 19:46:27
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
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id` DESC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of create_speech
-- ----------------------------

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS `file`;
CREATE TABLE `file`  (
  `file_id` int NOT NULL,
  `file_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_type` int NOT NULL,
  PRIMARY KEY (`file_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of file
-- ----------------------------

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
  `speech_id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `begin_time` datetime NOT NULL,
  PRIMARY KEY (`speech_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech
-- ----------------------------

-- ----------------------------
-- Table structure for speech_file
-- ----------------------------
DROP TABLE IF EXISTS `speech_file`;
CREATE TABLE `speech_file`  (
  `speech_id` int NOT NULL,
  `file_id` int NOT NULL,
  PRIMARY KEY (`speech_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech_file
-- ----------------------------

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
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_type` int NOT NULL,
  PRIMARY KEY (`user_id` DESC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '1231', 'hhh', 1);

-- ----------------------------
-- Table structure for user_file
-- ----------------------------
DROP TABLE IF EXISTS `user_file`;
CREATE TABLE `user_file`  (
  `user_id` int NOT NULL,
  `file_id` int NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_file
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
