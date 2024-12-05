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
  `khoiPhong_id` int NOT NULL,
  `tenLop` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `giaoVienChuNhiem_id` int DEFAULT NULL,
  `siSo` int NOT NULL,
  `hocKy_id` int NOT NULL,
  PRIMARY KEY (`maDsLop`),
  KEY `khoiPhong_id` (`khoiPhong_id`),
  KEY `giaoVienChuNhiem_id` (`giaoVienChuNhiem_id`),
  KEY `hocKy_id` (`hocKy_id`),
  CONSTRAINT `danh_sach_lop_ibfk_1` FOREIGN KEY (`khoiPhong_id`) REFERENCES `khoi_phong` (`id`),
  CONSTRAINT `danh_sach_lop_ibfk_2` FOREIGN KEY (`giaoVienChuNhiem_id`) REFERENCES `giao_vien` (`idGiaoVien`),
  CONSTRAINT `danh_sach_lop_ibfk_3` FOREIGN KEY (`hocKy_id`) REFERENCES `hoc_ky` (`idHocKy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_lop`
--

LOCK TABLES `danh_sach_lop` WRITE;
/*!40000 ALTER TABLE `danh_sach_lop` DISABLE KEYS */;
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
  `hoTen` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioiTinh` tinyint(1) NOT NULL,
  `ngaySinh` date NOT NULL,
  `diaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `taiKhoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `matKhau` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `idMonHoc` int NOT NULL,
  PRIMARY KEY (`idGiaoVien`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  UNIQUE KEY `taiKhoan` (`taiKhoan`),
  KEY `idMonHoc` (`idMonHoc`),
  CONSTRAINT `giao_vien_ibfk_1` FOREIGN KEY (`idMonHoc`) REFERENCES `mon_hoc` (`idMonHoc`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giao_vien`
--

LOCK TABLES `giao_vien` WRITE;
/*!40000 ALTER TABLE `giao_vien` DISABLE KEYS */;
INSERT INTO `giao_vien` VALUES (1,'Tô Quốc Bình',1,'2004-02-21','Thành phố Hồ Chí Minh','0762590966','toquocbinh2102@gmail.com','quocbinh2004','e10adc3949ba59abbe56e057f20f883e',1),(2,'Trần Huỳnh Sang',1,'2004-12-08','Thành phố Hồ Chí Minh','0792821011','Sangdbrr@gmail.com','huynhsang2004','e10adc3949ba59abbe56e057f20f883e',3),(3,'Trần Quốc Phong',0,'2004-10-30','Thành phố Hồ Chí Minh','0792821010','tqphong2004@gmail.com','quocphong2004','e10adc3949ba59abbe56e057f20f883e',2),(4,'Nguyễn Đăng Khôi',1,'1992-09-09','Hà Nội','0794521012','khoi123@gmail.com','dangkhoi1992','e10adc3949ba59abbe56e057f20f883e',1);
/*!40000 ALTER TABLE `giao_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giao_vien_chu_nhiem`
--

DROP TABLE IF EXISTS `giao_vien_chu_nhiem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giao_vien_chu_nhiem` (
  `idGiaoVienCN` int NOT NULL AUTO_INCREMENT,
  `idGiaoVien` int DEFAULT NULL,
  `idDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idGiaoVienCN`),
  KEY `idGiaoVien` (`idGiaoVien`),
  KEY `idDsLop` (`idDsLop`),
  CONSTRAINT `giao_vien_chu_nhiem_ibfk_1` FOREIGN KEY (`idGiaoVien`) REFERENCES `giao_vien` (`idGiaoVien`),
  CONSTRAINT `giao_vien_chu_nhiem_ibfk_2` FOREIGN KEY (`idDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giao_vien_chu_nhiem`
--

LOCK TABLES `giao_vien_chu_nhiem` WRITE;
/*!40000 ALTER TABLE `giao_vien_chu_nhiem` DISABLE KEYS */;
/*!40000 ALTER TABLE `giao_vien_chu_nhiem` ENABLE KEYS */;
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
  `diaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eMail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maDsLop` int DEFAULT NULL,
  PRIMARY KEY (`idHocSinh`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `eMail` (`eMail`),
  KEY `maDsLop` (`maDsLop`),
  CONSTRAINT `hoc_sinh_ibfk_1` FOREIGN KEY (`maDsLop`) REFERENCES `danh_sach_lop` (`maDsLop`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoc_sinh`
--

LOCK TABLES `hoc_sinh` WRITE;
/*!40000 ALTER TABLE `hoc_sinh` DISABLE KEYS */;
INSERT INTO `hoc_sinh` VALUES (1,'Tô Quốc Bình',1,'2009-02-21','Thành phố Hồ Chí Minh','0762590966','toquocbinh2102@gmail.com',NULL),(2,'Trần Quốc Phong',1,'2008-10-30','Thành phố Hồ Chí Minh','0792821010','tqphong2004@gmail.com',NULL);
/*!40000 ALTER TABLE `hoc_sinh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khoi_lop`
--

DROP TABLE IF EXISTS `khoi_lop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khoi_lop` (
  `idKhoiLop` int NOT NULL AUTO_INCREMENT,
  `tenKhoi` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idKhoiLop`),
  UNIQUE KEY `tenKhoi` (`tenKhoi`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khoi_lop`
--

LOCK TABLES `khoi_lop` WRITE;
/*!40000 ALTER TABLE `khoi_lop` DISABLE KEYS */;
INSERT INTO `khoi_lop` VALUES (1,'10'),(2,'11'),(3,'12');
/*!40000 ALTER TABLE `khoi_lop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khoi_phong`
--

DROP TABLE IF EXISTS `khoi_phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khoi_phong` (
  `id` int NOT NULL AUTO_INCREMENT,
  `khoiLop_id` int NOT NULL,
  `phongHoc_id` int NOT NULL,
  `buoiHoc` enum('SANG','CHIEU') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `khoiLop_id` (`khoiLop_id`),
  KEY `phongHoc_id` (`phongHoc_id`),
  CONSTRAINT `khoi_phong_ibfk_1` FOREIGN KEY (`khoiLop_id`) REFERENCES `khoi_lop` (`idKhoiLop`),
  CONSTRAINT `khoi_phong_ibfk_2` FOREIGN KEY (`phongHoc_id`) REFERENCES `phong_hoc` (`idPhongHoc`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khoi_phong`
--

LOCK TABLES `khoi_phong` WRITE;
/*!40000 ALTER TABLE `khoi_phong` DISABLE KEYS */;
INSERT INTO `khoi_phong` VALUES (1,1,1,'SANG'),(9,1,2,'SANG'),(10,2,3,'SANG'),(11,2,1,'CHIEU'),(12,3,2,'CHIEU'),(13,3,3,'CHIEU');
/*!40000 ALTER TABLE `khoi_phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mon_hoc`
--

DROP TABLE IF EXISTS `mon_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mon_hoc` (
  `idMonHoc` int NOT NULL AUTO_INCREMENT,
  `tenMonHoc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong_hoc`
--

LOCK TABLES `phong_hoc` WRITE;
/*!40000 ALTER TABLE `phong_hoc` DISABLE KEYS */;
INSERT INTO `phong_hoc` VALUES (1,'Phòng 101'),(2,'Phòng 102'),(3,'Phòng 201');
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

-- Dump completed on 2024-12-05 17:48:13
