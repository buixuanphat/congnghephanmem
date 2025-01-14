-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: manadb
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `danh_sach_lop`
--

DROP TABLE IF EXISTS `danh_sach_lop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_lop` (
  `maDsLop` int NOT NULL AUTO_INCREMENT,
  `idPhongHoc` int DEFAULT NULL,
  `tenLop` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `khoi` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `giaoVienChuNhiem_id` int DEFAULT NULL,
  `siSoHienTai` int NOT NULL,
  `siSo` int NOT NULL,
  `hocKy_id` int NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`maDsLop`),
  UNIQUE KEY `idPhongHoc` (`idPhongHoc`),
  UNIQUE KEY `tenLop` (`tenLop`),
  KEY `giaoVienChuNhiem_id` (`giaoVienChuNhiem_id`),
  KEY `hocKy_id` (`hocKy_id`),
  CONSTRAINT `danh_sach_lop_ibfk_1` FOREIGN KEY (`idPhongHoc`) REFERENCES `phong_hoc` (`idPhongHoc`),
  CONSTRAINT `danh_sach_lop_ibfk_2` FOREIGN KEY (`giaoVienChuNhiem_id`) REFERENCES `giao_vien` (`idGiaoVien`),
  CONSTRAINT `danh_sach_lop_ibfk_3` FOREIGN KEY (`hocKy_id`) REFERENCES `hoc_ky` (`idHocKy`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_lop`
--

LOCK TABLES `danh_sach_lop` WRITE;
/*!40000 ALTER TABLE `danh_sach_lop` DISABLE KEYS */;
INSERT INTO `danh_sach_lop` VALUES (4,1,'10A1','Khối 10',5,1,2,2,1),(5,3,'11A1','Khối 11',4,2,2,2,1),(6,2,'11A3','Khối 11',1,1,2,2,1),(7,4,'12A1','Khối 12',2,2,2,2,1);
/*!40000 ALTER TABLE `danh_sach_lop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giao_vien`
--

DROP TABLE IF EXISTS `giao_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giao_vien` (
  `idGiaoVien` int NOT NULL AUTO_INCREMENT,
  `hoTen` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `diaChi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `taiKhoan` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `matKhau` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `idMonHoc` int NOT NULL,
  PRIMARY KEY (`idGiaoVien`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  UNIQUE KEY `taiKhoan` (`taiKhoan`),
  KEY `idMonHoc` (`idMonHoc`),
  CONSTRAINT `giao_vien_ibfk_1` FOREIGN KEY (`idMonHoc`) REFERENCES `mon_hoc` (`idMonHoc`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giao_vien`
--

LOCK TABLES `giao_vien` WRITE;
/*!40000 ALTER TABLE `giao_vien` DISABLE KEYS */;
INSERT INTO `giao_vien` VALUES (1,'Tô Quốc Bình',1,'2004-02-21','Thành phố Hồ Chí Minh','0762590966','toquocbinh2102@gmail.com','quocbinh2004','e10adc3949ba59abbe56e057f20f883e',1),(2,'Trần Huỳnh Sang',1,'2004-12-08','Thành phố Hồ Chí Minh','0792821011','Sangdbrr@gmail.com','huynhsang2004','e10adc3949ba59abbe56e057f20f883e',3),(3,'Trần Quốc Phong',0,'2004-10-30','Thành phố Hồ Chí Minh','0792821010','tqphong2004@gmail.com','quocphong2004','e10adc3949ba59abbe56e057f20f883e',2),(4,'Nguyễn Đăng Khôi',1,'1992-09-09','Hà Nội','0794521012','khoi123@gmail.com','dangkhoi1992','e10adc3949ba59abbe56e057f20f883e',1),(5,'Ngô Quốc Quân',1,'1992-09-09','Thành phố Hồ Chí Minh','0123456785','quan123@gmail.com','quocquan','e10adc3949ba59abbe56e057f20f883e',1);
/*!40000 ALTER TABLE `giao_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giao_vien_day_hoc`
--

DROP TABLE IF EXISTS `giao_vien_day_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giao_vien_day_hoc` (
  `idGiaoVienDayHoc` int NOT NULL AUTO_INCREMENT,
  `idGiaoVien` int DEFAULT NULL,
  `idDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idGiaoVienDayHoc`),
  KEY `idGiaoVien` (`idGiaoVien`),
  KEY `idDsLop` (`idDsLop`),
  CONSTRAINT `giao_vien_day_hoc_ibfk_1` FOREIGN KEY (`idGiaoVien`) REFERENCES `giao_vien` (`idGiaoVien`),
  CONSTRAINT `giao_vien_day_hoc_ibfk_2` FOREIGN KEY (`idDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giao_vien_day_hoc`
--

LOCK TABLES `giao_vien_day_hoc` WRITE;
/*!40000 ALTER TABLE `giao_vien_day_hoc` DISABLE KEYS */;
INSERT INTO `giao_vien_day_hoc` VALUES (4,5,4),(5,3,4),(6,2,4),(7,4,5),(8,3,5),(9,2,5),(10,1,6),(11,3,6),(12,2,6),(13,2,7),(14,4,7),(15,3,7);
/*!40000 ALTER TABLE `giao_vien_day_hoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoc_ky`
--

DROP TABLE IF EXISTS `hoc_ky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoc_ky` (
  `idHocKy` int NOT NULL AUTO_INCREMENT,
  `namHoc` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hocKy` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idHocKy`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoc_ky`
--

LOCK TABLES `hoc_ky` WRITE;
/*!40000 ALTER TABLE `hoc_ky` DISABLE KEYS */;
INSERT INTO `hoc_ky` VALUES (1,'2024-2025','1'),(2,'2024-2025','2');
/*!40000 ALTER TABLE `hoc_ky` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoc_sinh`
--

DROP TABLE IF EXISTS `hoc_sinh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoc_sinh` (
  `idHocSinh` int NOT NULL AUTO_INCREMENT,
  `hoTen` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `khoi` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `diaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idHocSinh`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  KEY `maDsLop` (`maDsLop`),
  CONSTRAINT `hoc_sinh_ibfk_1` FOREIGN KEY (`maDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoc_sinh`
--

LOCK TABLES `hoc_sinh` WRITE;
/*!40000 ALTER TABLE `hoc_sinh` DISABLE KEYS */;
INSERT INTO `hoc_sinh` VALUES (1,'Trần Huỳnh Sá',1,'2009-02-12','Khối 10','Thành phố Hồ Chí Minh','0987654321','hsang1@gmail.com',4),(2,'Nguyễn Đăng Băng',0,'2008-03-02','Khối 11','Thành phố Hồ Chí Minh','0911342943','Tranthanhbaokhanh@gmail.com',5),(3,'Trần Quốc Pha',1,'2008-01-02','Khối 11','Hà Nội','0123456789','tqphong2004@gmail.com',5),(4,'Tô Quốc Ba',1,'2007-02-01','Khối 12','Thành phố Hồ Chí Minh','0564822138','toquocbinh2102@gmail.com',7),(5,'Nguyễn Đăng Khôi',1,'2007-04-12','Khối 12','Thành phố Hồ Chí Minh','0762590966','dang123@gmail.com',7),(6,'Nguyễn Đăng Tra',1,'2007-04-03','Khối 11','Hà Nội','0987654325','khoi3@gmail.com',6),(8,'Tô Quốc Can',1,'2009-01-04','Khối 10','Thành phố Hồ Chí Minh','0987654320','dangad123@gmail.com',4),(9,'Trần Huỳnh Duy',1,'2008-06-05','Khối 11','Thành phố Hồ Chí Minh','0762590066','hduy1@gmail.com',6);
/*!40000 ALTER TABLE `hoc_sinh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mon_hoc`
--

DROP TABLE IF EXISTS `mon_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mon_hoc` (
  `idMonHoc` int NOT NULL AUTO_INCREMENT,
  `tenMonHoc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idMonHoc`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mon_hoc`
--

LOCK TABLES `mon_hoc` WRITE;
/*!40000 ALTER TABLE `mon_hoc` DISABLE KEYS */;
INSERT INTO `mon_hoc` VALUES (1,'Toán'),(2,'Văn'),(3,'Anh');
/*!40000 ALTER TABLE `mon_hoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhan_vien`
--

DROP TABLE IF EXISTS `nhan_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhan_vien` (
  `idNhanVien` int NOT NULL AUTO_INCREMENT,
  `hoTen` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `diaChi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `vaiTro` enum('ADMIN','NHANVIENTIEPNHAN','GIAOVIEN','NGUOIQUANTRI') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `taiKhoan` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `matKhau` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idNhanVien`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  UNIQUE KEY `taiKhoan` (`taiKhoan`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhan_vien`
--

LOCK TABLES `nhan_vien` WRITE;
/*!40000 ALTER TABLE `nhan_vien` DISABLE KEYS */;
INSERT INTO `nhan_vien` VALUES (1,'Tô Quốc Bình',1,'2004-02-21','Thành phố Hồ Chí Minh','0762590966','toquocbinh2102@gmail.com','NHANVIENTIEPNHAN','quocbinh','e10adc3949ba59abbe56e057f20f883e'),(3,'Trần Quốc Phong',1,'2004-10-30','Thành phố Hồ Chí Minh','0799773010','toquocphong2102@gmail.com','NGUOIQUANTRI','quocphong','e10adc3949ba59abbe56e057f20f883e');
/*!40000 ALTER TABLE `nhan_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phong_hoc`
--

DROP TABLE IF EXISTS `phong_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phong_hoc` (
  `idPhongHoc` int NOT NULL AUTO_INCREMENT,
  `tenPhong` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idPhongHoc`),
  UNIQUE KEY `tenPhong` (`tenPhong`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong_hoc`
--

LOCK TABLES `phong_hoc` WRITE;
/*!40000 ALTER TABLE `phong_hoc` DISABLE KEYS */;
INSERT INTO `phong_hoc` VALUES (1,'A101'),(2,'A102'),(3,'A103'),(4,'A104'),(5,'A105'),(6,'B101'),(7,'B102'),(8,'B103'),(9,'B104'),(10,'B105'),(11,'C101'),(12,'C102'),(13,'C103'),(14,'C104'),(15,'C105');
/*!40000 ALTER TABLE `phong_hoc` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09  9:54:21
