/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.6-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: totem_ia
-- ------------------------------------------------------
-- Server version	11.8.6-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add cliente',7,'add_cliente'),
(26,'Can change cliente',7,'change_cliente'),
(27,'Can delete cliente',7,'delete_cliente'),
(28,'Can view cliente',7,'view_cliente'),
(29,'Can add mesa',8,'add_mesa'),
(30,'Can change mesa',8,'change_mesa'),
(31,'Can delete mesa',8,'delete_mesa'),
(32,'Can view mesa',8,'view_mesa'),
(33,'Can add turno',9,'add_turno'),
(34,'Can change turno',9,'change_turno'),
(35,'Can delete turno',9,'delete_turno'),
(36,'Can view turno',9,'view_turno'),
(37,'Can add log atencion',10,'add_logatencion'),
(38,'Can change log atencion',10,'change_logatencion'),
(39,'Can delete log atencion',10,'delete_logatencion'),
(40,'Can view log atencion',10,'view_logatencion'),
(41,'Can add Logo Pantalla',11,'add_logopantalla'),
(42,'Can change Logo Pantalla',11,'change_logopantalla'),
(43,'Can delete Logo Pantalla',11,'delete_logopantalla'),
(44,'Can view Logo Pantalla',11,'view_logopantalla'),
(45,'Can add Marquesina Pantalla',12,'add_marquesinapantalla'),
(46,'Can change Marquesina Pantalla',12,'change_marquesinapantalla'),
(47,'Can delete Marquesina Pantalla',12,'delete_marquesinapantalla'),
(48,'Can view Marquesina Pantalla',12,'view_marquesinapantalla'),
(49,'Can add Configuración Video',13,'add_configvideopantalla'),
(50,'Can change Configuración Video',13,'change_configvideopantalla'),
(51,'Can delete Configuración Video',13,'delete_configvideopantalla'),
(52,'Can view Configuración Video',13,'view_configvideopantalla'),
(53,'Can add Video Pantalla',14,'add_videopantalla'),
(54,'Can change Video Pantalla',14,'change_videopantalla'),
(55,'Can delete Video Pantalla',14,'delete_videopantalla'),
(56,'Can view Video Pantalla',14,'view_videopantalla'),
(57,'Can add Configuración Apariencia',15,'add_configapariencia'),
(58,'Can change Configuración Apariencia',15,'change_configapariencia'),
(59,'Can delete Configuración Apariencia',15,'delete_configapariencia'),
(60,'Can view Configuración Apariencia',15,'view_configapariencia');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$01EW9S7Jdj7txj1lnfPZcy$3aiSWvc/7X+31Q+rq/5ogpRSUL7rbF+oJQxzsFni4hk=','2026-04-01 01:27:04.799541',1,'admin','','','admin@totem.cl',1,1,'2026-03-18 20:31:52.169000'),
(2,'pbkdf2_sha256$1000000$QfSWmnSuqNne4lmi64IY5Z$l8oEM3pddlorH7w69kn+hFpmLwBxsmGzwVmPySvwWPM=','2026-04-01 01:24:05.602240',0,'usuario1','Marco','Arevalo','',0,1,'2026-03-19 14:15:45.000000'),
(3,'pbkdf2_sha256$1000000$7TXKR3ctSXn7qXQQkBhpTn$8uGiZ+WOx3JrOSFqAQHewBdAy8JFBnGHkqUFgFdacMI=','2026-03-31 18:36:41.233000',0,'usuario2','','','',0,1,'2026-03-19 16:44:26.000000'),
(4,'pbkdf2_sha256$1000000$r0CqJMweRJtRHppM9mIspP$f5x0JmI5ZjdifTeX5w10LMDtwHjtmTaPhqfaZWetgkM=','2026-03-19 16:53:57.855000',0,'usuario3','','','',0,1,'2026-03-19 16:45:00.894000'),
(5,'pbkdf2_sha256$1000000$BorlcBcWev5bsUQb9I9B3o$h9RmcS8olsng2lh7Hc0dxqXckwEIJtTFIvuL5ylo700=',NULL,0,'smura','Sara','Mura','',0,1,'2026-03-31 20:49:43.000000'),
(6,'pbkdf2_sha256$1000000$gJhEs8iUmZZHDHyozwlDWg$JZsoI9dbFMDRFReoBRgGs+e2R52hrg5FmirVRQ86NvI=',NULL,0,'ealcala','Emily','Alcalá','',0,1,'2026-03-31 20:49:45.633000'),
(7,'pbkdf2_sha256$1000000$yHsHf2jdfmXGLmZ3hUcXD5$7QjzyS9xE0mEUDwOLFPdpuoUZA4GE9JzJJ95M7ie3Mg=',NULL,0,'bmorales','Benjamin','Morales','',0,1,'2026-03-31 20:49:47.217000'),
(8,'pbkdf2_sha256$1000000$cU0g9Hj27dhwJpgS0T4TpV$8t2Gl/9OvCD0VGUYuHX1a1vKo5Jk61WOKRJ2wRIO2AE=',NULL,0,'svalenzuela','Sofia','Valenzuela','',0,1,'2026-03-31 20:49:48.000000'),
(9,'pbkdf2_sha256$1000000$hvCPhuC0ew4W0BTjTauw9e$vKrYv0vKtAs/RZCwWipfi0yhAt5mXzYTEXB3BqVLg7Q=',NULL,0,'arojas','Aylin','Rojas','',0,1,'2026-03-31 20:49:49.882000'),
(10,'pbkdf2_sha256$1000000$ByF8Z9oPy5Av4DUygkVAa6$Pv29L1hz4KMmX3GP6LprUabDIcrJTY59Z9Xl20k/61g=',NULL,0,'afuentes','Almendra','Fuentes','',0,1,'2026-03-31 20:49:50.993000'),
(11,'pbkdf2_sha256$1000000$e8ZYC312LV5sB02PjuO1Pk$2+3Aoo/HwKE+xlLYVXIXsU7OjXf7EFdLuFSszmIerTw=',NULL,0,'lpizarro','Lissette','Pizarro','',0,1,'2026-03-31 20:49:52.091000'),
(12,'pbkdf2_sha256$1000000$InTN8FIWWD1Hsfqmdg9H63$+yTMXgR++E08NHa6MzpVi6hD/B7UpoWaNskp7jNPdac=',NULL,0,'savalos','Sofia','Avalos','',0,1,'2026-03-31 20:49:53.000000'),
(13,'pbkdf2_sha256$1000000$ILIQHjLWNrjQrjy7uWOmQC$V8DAsVYmeLYSytGUocakt2yYrJaSuucIE7nLgZsJTxE=',NULL,0,'agomez','Antonella','Gomez','',0,1,'2026-03-31 20:49:54.228000'),
(14,'pbkdf2_sha256$1000000$bslY7E543pAxufvQstghzh$BTnWpj2OxTnOvKo5Ti9BaM5y1rYf6ZJZmrva73/p96g=',NULL,0,'jastudillo','Jean','Astudillo','',0,1,'2026-03-31 20:49:55.317000'),
(15,'pbkdf2_sha256$1000000$Rg0Hw3AH5jbQKvDuJd0IyP$NS5jm6J+99tJGHOybPyKYMDfYUrYqGNcz2IpBryHeM4=',NULL,0,'gcuellar','German','Cuellar','',0,1,'2026-03-31 20:49:56.464000'),
(16,'pbkdf2_sha256$1000000$yioGgZE8wjL8qmW9VVqPKh$CiDQuanaUX3HhMsbA7iDcCfuYkOqrkHU+OFpMsyoemg=',NULL,0,'agalleguillos','Amanda','Galleguillos','',0,1,'2026-03-31 20:49:57.497000'),
(17,'pbkdf2_sha256$1000000$wfekvs8dyf2HrK2LScuBK2$9Vxy3FS5+c7zx4Ecx2Z2Q/4j4kVgCmVvI4uNUJPbqZQ=',NULL,0,'maranda','Mayra','Aranda','',0,1,'2026-03-31 20:49:58.000000'),
(18,'pbkdf2_sha256$1000000$Cy8aE6yNuVkFqZSrPG3rfr$1AioOjZ4jlao9eZediqtvw/28H5hmgAX8uAYZQFp/iA=',NULL,0,'laraya','Lissette','Araya','',0,1,'2026-03-31 20:49:59.639000'),
(19,'pbkdf2_sha256$1000000$JAaEKXhmwzUjXoMKpe6DC0$w0W4UOVPuZ8fl62z3jiAuWPwioP0iQXUMzETjuGwAbg=',NULL,0,'idiaz','Ignacia','Díaz Cruz','',0,1,'2026-03-31 20:50:00.709000'),
(20,'pbkdf2_sha256$1000000$RXaf5Z3lEuuOXyicMo0Wn5$AXycDmX4/OtTsSRBStAmtla+5clnmVOO48u733ZgyKg=',NULL,0,'ijaque','Isidora','Jaque','',0,1,'2026-03-31 20:50:01.776000'),
(21,'pbkdf2_sha256$1000000$sEaQArUlrzIEqlWTqPJI3g$Pegn0hp5Pa0q4Ti9It4uWlXXaG+/mVuWdHIrRpqhCcQ=',NULL,0,'jvalenzuela','Javiera','Valenzuela','',0,1,'2026-03-31 20:50:02.817000'),
(22,'pbkdf2_sha256$1000000$AWMYx0zbKzc4ZtqMSZH5NW$7FrpQ8dbwoY3QDMQXdQv6ShePwWWEL8mSZEbK1SmAvM=',NULL,0,'nmedina','Nair','Medina','',0,1,'2026-03-31 20:50:03.000000'),
(23,'pbkdf2_sha256$1000000$NeEGTRU8kvPmpTOasfcJTJ$5ZsSU2zSuraNA8wQFkIN7OD5qbpza76iFvXOn7Q47Z4=',NULL,0,'ejimenez','Escarlen','Jimenez','',0,1,'2026-03-31 20:50:04.947000'),
(24,'pbkdf2_sha256$1000000$PbmQnT86PTke7s6cVnUuZg$vOWRmhy9yJ4RGPGuqAxBdMIC5c4+tKn6XbBR+BFd600=',NULL,0,'cavila','Constanza','Avila','',0,1,'2026-03-31 20:50:07.588000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_cliente`
--

DROP TABLE IF EXISTS `core_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_cliente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rut` varchar(12) NOT NULL,
  `nombre_completo` varchar(200) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `telefono` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `observaciones` longtext NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_cliente`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_cliente` WRITE;
/*!40000 ALTER TABLE `core_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_cliente` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_configapariencia`
--

DROP TABLE IF EXISTS `core_configapariencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_configapariencia` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pantalla_fondo` varchar(20) NOT NULL,
  `pantalla_call_grad1` varchar(20) NOT NULL,
  `pantalla_call_grad2` varchar(20) NOT NULL,
  `pantalla_codigo_color` varchar(20) NOT NULL,
  `pantalla_codigo_fuente` varchar(100) NOT NULL,
  `pantalla_codigo_tamano` varchar(20) NOT NULL,
  `pantalla_nombre_color` varchar(20) NOT NULL,
  `pantalla_nombre_fuente` varchar(100) NOT NULL,
  `pantalla_nombre_tamano` varchar(20) NOT NULL,
  `pantalla_mesa_color` varchar(20) NOT NULL,
  `pantalla_mesa_fuente` varchar(100) NOT NULL,
  `pantalla_mesa_tamano` varchar(20) NOT NULL,
  `pantalla_espera_grad1` varchar(20) NOT NULL,
  `pantalla_espera_grad2` varchar(20) NOT NULL,
  `pantalla_historial_codigo` varchar(20) NOT NULL,
  `pantalla_historial_nombre` varchar(20) NOT NULL,
  `pantalla_historial_mesa` varchar(20) NOT NULL,
  `nav_grad1` varchar(20) NOT NULL,
  `nav_grad2` varchar(20) NOT NULL,
  `totem_fondo_grad1` varchar(20) NOT NULL,
  `totem_fondo_grad2` varchar(20) NOT NULL,
  `totem_fondo_grad3` varchar(20) NOT NULL,
  `totem_header_grad1` varchar(20) NOT NULL,
  `totem_header_grad2` varchar(20) NOT NULL,
  `btn_llamar_grad1` varchar(20) NOT NULL,
  `btn_llamar_grad2` varchar(20) NOT NULL,
  `btn_completar_grad1` varchar(20) NOT NULL,
  `btn_completar_grad2` varchar(20) NOT NULL,
  `btn_guardar_grad1` varchar(20) NOT NULL,
  `btn_guardar_grad2` varchar(20) NOT NULL,
  `confirmado_esperando_grad1` varchar(20) NOT NULL,
  `confirmado_esperando_grad2` varchar(20) NOT NULL,
  `confirmado_llamado_grad1` varchar(20) NOT NULL,
  `confirmado_llamado_grad2` varchar(20) NOT NULL,
  `confirmado_completado_grad1` varchar(20) NOT NULL,
  `confirmado_completado_grad2` varchar(20) NOT NULL,
  `confirmado_cancelado_grad1` varchar(20) NOT NULL,
  `confirmado_cancelado_grad2` varchar(20) NOT NULL,
  `pantalla_footer_texto` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_configapariencia`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_configapariencia` WRITE;
/*!40000 ALTER TABLE `core_configapariencia` DISABLE KEYS */;
INSERT INTO `core_configapariencia` VALUES
(1,'#0d1b2a','#1565c0','#0d47a1','#ffffff','Roboto, sans-serif','10rem','#ffca28','Roboto, sans-serif','3rem','#81d4fa','Roboto, sans-serif','4rem','#ff6f00','#ff8f00','#ffca28','#e0e0e0','#81d4fa','#1565c0','#0d47a1','#0d47a1','#1565c0','#1e88e5','#ff6f00','#ff8f00','#ff6f00','#ff8f00','#2e7d32','#43a047','#1565c0','#1e88e5','#2e7d32','#43a047','#e65100','#ff6f00','#1565c0','#1e88e5','#b71c1c','#e53935','Crea Empresas - Fab Inacap Copiapo 2026');
/*!40000 ALTER TABLE `core_configapariencia` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_configvideopantalla`
--

DROP TABLE IF EXISTS `core_configvideopantalla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_configvideopantalla` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modo_reproduccion` varchar(20) NOT NULL,
  `volumen` int(11) NOT NULL,
  `habilitado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_configvideopantalla`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_configvideopantalla` WRITE;
/*!40000 ALTER TABLE `core_configvideopantalla` DISABLE KEYS */;
INSERT INTO `core_configvideopantalla` VALUES
(1,'aleatorio',30,1);
/*!40000 ALTER TABLE `core_configvideopantalla` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_logatencion`
--

DROP TABLE IF EXISTS `core_logatencion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_logatencion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `accion` varchar(100) NOT NULL,
  `detalle` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `turno_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_logatencion_usuario_id_2b16b7e5_fk_auth_user_id` (`usuario_id`),
  KEY `core_logatencion_turno_id_05a3be10_fk_core_turno_id` (`turno_id`),
  CONSTRAINT `core_logatencion_turno_id_05a3be10_fk_core_turno_id` FOREIGN KEY (`turno_id`) REFERENCES `core_turno` (`id`),
  CONSTRAINT `core_logatencion_usuario_id_2b16b7e5_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_logatencion`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_logatencion` WRITE;
/*!40000 ALTER TABLE `core_logatencion` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_logatencion` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_logopantalla`
--

DROP TABLE IF EXISTS `core_logopantalla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_logopantalla` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_logopantalla`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_logopantalla` WRITE;
/*!40000 ALTER TABLE `core_logopantalla` DISABLE KEYS */;
INSERT INTO `core_logopantalla` VALUES
(1,'Inacap','logos/logo_inacap.png',0,1),
(2,'SII','logos/logo_sii.png',1,0),
(3,'Logo Blanco','logos/logo-blanco-mobile.png',1,0);
/*!40000 ALTER TABLE `core_logopantalla` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_marquesinapantalla`
--

DROP TABLE IF EXISTS `core_marquesinapantalla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_marquesinapantalla` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `texto` varchar(500) NOT NULL,
  `color` varchar(20) NOT NULL,
  `velocidad` int(11) NOT NULL,
  `tamano_fuente` varchar(10) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_marquesinapantalla`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_marquesinapantalla` WRITE;
/*!40000 ALTER TABLE `core_marquesinapantalla` DISABLE KEYS */;
INSERT INTO `core_marquesinapantalla` VALUES
(1,'Bienvenidos a Inacap - Solicite su número leyendo el QR','#ffffff',20,'2rem',1,1),
(2,'Necesitamos nos ayuden con sus datos, regístrelos en la aplicación','#F5E427',20,'1.5rem',1,2),
(3,'🎓 Bienvenidos a Inacap 🎓 — Solicite su turno en el totem 📱','#ffffff',20,'3em',0,3);
/*!40000 ALTER TABLE `core_marquesinapantalla` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_mesa`
--

DROP TABLE IF EXISTS `core_mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_mesa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `atendida_por_id` int(11) DEFAULT NULL,
  `edad_preferencial` int(11) NOT NULL,
  `preferencial` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_mesa_atendida_por_id_17798d81_fk_auth_user_id` (`atendida_por_id`),
  CONSTRAINT `core_mesa_atendida_por_id_17798d81_fk_auth_user_id` FOREIGN KEY (`atendida_por_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_mesa`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_mesa` WRITE;
/*!40000 ALTER TABLE `core_mesa` DISABLE KEYS */;
INSERT INTO `core_mesa` VALUES
(1,'Mesa 1',1,2,60,1),
(2,'Mesa 2',1,NULL,60,1),
(3,'Mesa 3',1,NULL,60,0),
(4,'Mesa 4',1,NULL,60,0);
/*!40000 ALTER TABLE `core_mesa` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_turno`
--

DROP TABLE IF EXISTS `core_turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_turno` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(5) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  `llamado_en` datetime(6) DEFAULT NULL,
  `completado_en` datetime(6) DEFAULT NULL,
  `atendido_por_id` int(11) DEFAULT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `mesa_id` bigint(20) DEFAULT NULL,
  `es_preferencial` tinyint(1) NOT NULL,
  `motivo_preferencial` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `core_turno_atendido_por_id_580bc00d_fk_auth_user_id` (`atendido_por_id`),
  KEY `core_turno_cliente_id_fd853b13_fk_core_cliente_id` (`cliente_id`),
  KEY `core_turno_mesa_id_836cd71b_fk_core_mesa_id` (`mesa_id`),
  CONSTRAINT `core_turno_atendido_por_id_580bc00d_fk_auth_user_id` FOREIGN KEY (`atendido_por_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_turno_cliente_id_fd853b13_fk_core_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `core_cliente` (`id`),
  CONSTRAINT `core_turno_mesa_id_836cd71b_fk_core_mesa_id` FOREIGN KEY (`mesa_id`) REFERENCES `core_mesa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_turno`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_turno` WRITE;
/*!40000 ALTER TABLE `core_turno` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_turno` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_videopantalla`
--

DROP TABLE IF EXISTS `core_videopantalla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_videopantalla` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `url` varchar(200) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_videopantalla`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_videopantalla` WRITE;
/*!40000 ALTER TABLE `core_videopantalla` DISABLE KEYS */;
INSERT INTO `core_videopantalla` VALUES
(2,'prueba 2','https://vimeo.com/41789817',1,2),
(3,'prueba3','https://vimeo.com/153576526',1,1),
(4,'ejemplo 3','https://vimeo.com/83364353',1,3),
(5,'ejemplo 4','https://vimeo.com/214260971',1,4),
(6,'ejemplo 5','https://vimeo.com/352630264',1,5),
(7,'ejemplo 6','https://vimeo.com/19623852',1,6),
(8,'ejemplo 7','https://vimeo.com/145056220',1,7),
(9,'video 8','https://vimeo.com/421578474',1,8),
(10,'video 9','https://vimeo.com/90036109',1,9),
(11,'el chavo 1','https://vimeo.com/370507175',1,10),
(12,'el chavo 2','https://vimeo.com/761233129',1,11),
(13,'el chavo 3','https://vimeo.com/373262324',1,13),
(14,'el chavo 4','https://vimeo.com/371007748',1,12),
(15,'el chavo 5','https://vimeo.com/370529787?fl=pl&fe=sh',1,15),
(16,'el chavo 6','https://vimeo.com/371139296',1,14);
/*!40000 ALTER TABLE `core_videopantalla` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES
(1,'2026-03-19 14:14:14.173000','1','Mesa 1 ⭐',2,'[{\"changed\": {\"fields\": [\"Preferencial\"]}}]',8,1),
(2,'2026-03-19 14:15:46.186000','2','usuario1',1,'[{\"added\": {}}]',4,1),
(3,'2026-03-19 14:16:06.094000','2','usuario1',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),
(4,'2026-03-19 14:16:15.744000','1','Mesa 1 ⭐',2,'[{\"changed\": {\"fields\": [\"Atendida por\"]}}]',8,1),
(5,'2026-03-19 16:44:26.799000','3','usuario2',1,'[{\"added\": {}}]',4,1),
(6,'2026-03-19 16:44:33.664000','3','usuario2',2,'[]',4,1),
(7,'2026-03-19 16:45:01.559000','4','usuario3',1,'[{\"added\": {}}]',4,1),
(8,'2026-03-31 16:54:21.420000','1','Inacap',1,'[{\"added\": {}}]',11,1),
(9,'2026-03-31 16:54:31.457000','2','SII',1,'[{\"added\": {}}]',11,1),
(10,'2026-03-31 16:54:43.806000','1','Inacap',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',11,1),
(11,'2026-03-31 16:56:24.424000','3','Logo Blanco',1,'[{\"added\": {}}]',11,1),
(12,'2026-03-31 16:56:29.404000','1','Inacap',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',11,1),
(13,'2026-03-31 17:07:58.364000','1','Bienvenidos a Inacap - Solicite su nùmero leyendo ',1,'[{\"added\": {}}]',12,1),
(14,'2026-03-31 17:17:37.208000','1','PRueba1',1,'[{\"added\": {}}]',14,1),
(15,'2026-03-31 17:26:04.677000','1','PRueba1',2,'[{\"changed\": {\"fields\": [\"Url\"]}}]',14,1),
(16,'2026-03-31 18:14:10.415000','1','PRueba1',2,'[{\"changed\": {\"fields\": [\"Url\"]}}]',14,1),
(17,'2026-03-31 18:14:41.319000','2','prueba 2',1,'[{\"added\": {}}]',14,1),
(18,'2026-03-31 18:14:47.843000','1','PRueba1',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(19,'2026-03-31 18:15:29.584000','3','prueba3',1,'[{\"added\": {}}]',14,1),
(20,'2026-03-31 18:19:20.788000','2','prueba 2',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(21,'2026-03-31 18:19:20.789000','1','PRueba1',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(22,'2026-03-31 18:19:20.790000','3','prueba3',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(23,'2026-03-31 18:19:41.598000','1','PRueba1',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',14,1),
(24,'2026-03-31 19:21:14.420000','4','ejemplo 3',1,'[{\"added\": {}}]',14,1),
(25,'2026-03-31 19:21:50.535000','5','ejemplo 4',1,'[{\"added\": {}}]',14,1),
(26,'2026-03-31 19:22:14.473000','6','ejemplo 5',1,'[{\"added\": {}}]',14,1),
(27,'2026-03-31 19:22:59.998000','7','ejemplo 6',1,'[{\"added\": {}}]',14,1),
(28,'2026-03-31 19:23:36.509000','8','ejemplo 7',1,'[{\"added\": {}}]',14,1),
(29,'2026-03-31 19:24:38.722000','9','video 8',1,'[{\"added\": {}}]',14,1),
(30,'2026-03-31 19:24:48.025000','9','video 8',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(31,'2026-03-31 19:25:00.743000','8','ejemplo 7',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(32,'2026-03-31 19:25:00.745000','7','ejemplo 6',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(33,'2026-03-31 19:25:00.746000','9','video 8',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(34,'2026-03-31 19:25:53.146000','10','video 9',1,'[{\"added\": {}}]',14,1),
(35,'2026-03-31 19:28:15.233000','11','el chavo 1',1,'[{\"added\": {}}]',14,1),
(36,'2026-03-31 19:28:42.273000','12','el chavo 2',1,'[{\"added\": {}}]',14,1),
(37,'2026-03-31 19:29:09.938000','13','el chavo 3',1,'[{\"added\": {}}]',14,1),
(38,'2026-03-31 19:29:44.824000','14','el chavo 4',1,'[{\"added\": {}}]',14,1),
(39,'2026-03-31 19:29:58.779000','13','el chavo 3',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(40,'2026-03-31 19:31:08.043000','15','el chavo 5',1,'[{\"added\": {}}]',14,1),
(41,'2026-03-31 19:31:51.285000','16','el chavo 6',1,'[{\"added\": {}}]',14,1),
(42,'2026-03-31 19:33:26.859000','17','el chapulin 1',1,'[{\"added\": {}}]',14,1),
(43,'2026-03-31 19:34:31.481000','17','el chapulin 1',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(44,'2026-03-31 19:34:43.903000','18','el chapulin',1,'[{\"added\": {}}]',14,1),
(45,'2026-03-31 19:36:34.412000','19','el chapulin 3',1,'[{\"added\": {}}]',14,1),
(46,'2026-03-31 19:37:18.213000','18','el chapulin',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',14,1),
(47,'2026-03-31 19:37:34.211000','20','el chapulin 19',1,'[{\"added\": {}}]',14,1),
(48,'2026-03-31 19:39:25.624000','19','el chapulin 3',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',14,1),
(49,'2026-03-31 19:39:34.417000','19','el chapulin 3',3,'',14,1),
(50,'2026-03-31 19:39:49.970000','1','PRueba1',3,'',14,1),
(51,'2026-03-31 20:05:42.213000','1','Config Video - aleatorio - Vol:30',2,'[{\"changed\": {\"fields\": [\"Modo reproduccion\"]}}]',13,1),
(52,'2026-03-31 20:20:01.397000','20','el chapulin 19',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',14,1),
(53,'2026-03-31 20:22:47.572000','18','el chapulin',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',14,1),
(54,'2026-03-31 20:27:54.836000','18','el chapulin',3,'',14,1),
(55,'2026-03-31 20:28:02.427000','20','el chapulin 19',3,'',14,1),
(56,'2026-03-31 20:28:11.986000','17','el chapulin 1',3,'',14,1),
(57,'2026-03-31 20:47:37.086000','26','Jorge arias ()',3,'',7,1),
(58,'2026-03-31 20:47:37.086000','25','Eduardo Arevalo Salgado ()',3,'',7,1),
(59,'2026-03-31 20:47:37.086000','24','BREND KYIEIBEEEED DE AREVALO ()',3,'',7,1),
(60,'2026-03-31 20:47:37.086000','23','Mauricio cordova ()',3,'',7,1),
(61,'2026-03-31 20:47:37.086000','22','ALEX VELKAN (22.721.951-3)',3,'',7,1),
(62,'2026-03-31 20:47:37.086000','21','Marco Arévalo ()',3,'',7,1),
(63,'2026-03-31 20:47:37.086000','20','ISABEL VALENCIA ANTONIA (22.518.625-1)',3,'',7,1),
(64,'2026-03-31 20:47:37.086000','19','ANGELLO BASSI ()',3,'',7,1),
(65,'2026-03-31 20:47:37.086000','18','Juan Pino ()',3,'',7,1),
(66,'2026-03-31 20:47:37.086000','17','Juan Pino ()',3,'',7,1),
(67,'2026-03-31 20:47:37.086000','16','MARCO AREVALO ZAMBRANO ()',3,'',7,1),
(68,'2026-03-31 20:47:37.086000','15','MARCO AREVALO ZAMBRANO ()',3,'',7,1),
(69,'2026-03-31 20:47:37.086000','14','ANGELLO BASSI (10.630.535-8)',3,'',7,1),
(70,'2026-03-31 20:47:37.086000','13','Juan perez (6774511-6)',3,'',7,1),
(71,'2026-03-31 20:47:37.086000','12','ANGELLO BASSI (10.630.535-8)',3,'',7,1),
(72,'2026-03-31 20:47:37.086000','11','BREND KYIEIBEEEED DE AREVALO (28.635.776-8)',3,'',7,1),
(73,'2026-03-31 20:47:37.086000','10','ANGELLO bassi scola (10.630.535-8)',3,'',7,1),
(74,'2026-03-31 20:47:37.086000','9','Miguel de unamuno (1-9)',3,'',7,1),
(75,'2026-03-31 20:47:37.086000','8','Cristian suazo (99795544-6)',3,'',7,1),
(76,'2026-03-31 20:47:37.086000','7','Patricio Arevalo Zambrano (13.805.306-7)',3,'',7,1),
(77,'2026-03-31 20:47:37.086000','6','Marco Arévalo (14333671-9)',3,'',7,1),
(78,'2026-03-31 20:47:37.086000','5','Eduardo Arevalo Salgado (7664511-6)',3,'',7,1),
(79,'2026-03-31 20:47:37.086000','4','Eduardo Arevalo Salgado (7664511-6)',3,'',7,1),
(80,'2026-03-31 20:47:37.087000','3','ANTONI IACNK ZAMBRANO MARCO (14.333.671-9)',3,'',7,1),
(81,'2026-03-31 20:47:37.087000','2','MARCO ANTONI KZAMBRANO S (14.333.671-9)',3,'',7,1),
(82,'2026-03-31 20:47:37.087000','1','BREND KYIEIBEEEED DE AREVALO (28.635.776-8)',3,'',7,1),
(83,'2026-03-31 20:51:02.758000','8','svalenzuela',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),
(84,'2026-03-31 20:51:12.348000','5','smura',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),
(85,'2026-03-31 20:51:21.900000','12','savalos',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),
(86,'2026-03-31 20:51:30.204000','22','nmedina',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),
(87,'2026-03-31 20:51:38.999000','17','maranda',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),
(88,'2026-03-31 20:55:11.487000','2','Necesitamos nos ayuden con sus datos, registrelos ',1,'[{\"added\": {}}]',12,1),
(89,'2026-03-31 20:59:44.490000','2','Necesitamos nos ayuden con sus datos, registrelos ',2,'[{\"changed\": {\"fields\": [\"Orden\"]}}]',12,1),
(90,'2026-03-31 20:59:44.491000','1','Bienvenidos a Inacap - Solicite su nùmero leyendo ',2,'[{\"changed\": {\"fields\": [\"Tamano fuente\", \"Orden\"]}}]',12,1),
(91,'2026-03-31 21:00:13.253000','2','Necesitamos nos ayuden con sus datos, registrelos ',2,'[]',12,1),
(92,'2026-03-31 21:00:21.355000','1','Bienvenidos a Inacap - Solicite su número leyendo ',2,'[{\"changed\": {\"fields\": [\"Texto\"]}}]',12,1),
(93,'2026-03-31 21:01:11.590000','2','Necesitamos nos ayuden con sus datos, regístrelos ',2,'[{\"changed\": {\"fields\": [\"Texto\"]}}]',12,1),
(94,'2026-03-31 23:49:34.532000','1','Configuración de Apariencia',2,'[{\"changed\": {\"fields\": [\"Pantalla footer texto\"]}}]',15,1),
(95,'2026-03-31 23:51:14.394000','2','Necesitamos nos ayuden con sus datos, regístrelos ',2,'[{\"changed\": {\"fields\": [\"Texto\"]}}]',12,1),
(96,'2026-03-31 23:52:45.094000','3','🎓 Bienvenidos a Inacap 🎓 — Solicite su turno en el',1,'[{\"added\": {}}]',12,1),
(97,'2026-03-31 23:53:22.228000','3','🎓 Bienvenidos a Inacap 🎓 — Solicite su turno en el',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',12,1),
(98,'2026-03-31 23:53:36.454000','1','Inacap',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',11,1),
(99,'2026-03-31 23:54:05.639000','1','Inacap',2,'[{\"changed\": {\"fields\": [\"Activo\"]}}]',11,1),
(100,'2026-03-31 23:56:23.639000','27','Marco Arévalo ()',3,'',7,1),
(101,'2026-04-01 01:27:21.937400','1','ANGELLO BASSI ()',3,'',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(7,'core','cliente'),
(15,'core','configapariencia'),
(13,'core','configvideopantalla'),
(10,'core','logatencion'),
(11,'core','logopantalla'),
(12,'core','marquesinapantalla'),
(8,'core','mesa'),
(9,'core','turno'),
(14,'core','videopantalla'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-04-01 01:18:51.517558'),
(2,'auth','0001_initial','2026-04-01 01:18:51.960338'),
(3,'admin','0001_initial','2026-04-01 01:18:52.059037'),
(4,'admin','0002_logentry_remove_auto_add','2026-04-01 01:18:52.068673'),
(5,'admin','0003_logentry_add_action_flag_choices','2026-04-01 01:18:52.078430'),
(6,'contenttypes','0002_remove_content_type_name','2026-04-01 01:18:52.146406'),
(7,'auth','0002_alter_permission_name_max_length','2026-04-01 01:18:52.193561'),
(8,'auth','0003_alter_user_email_max_length','2026-04-01 01:18:52.224235'),
(9,'auth','0004_alter_user_username_opts','2026-04-01 01:18:52.233570'),
(10,'auth','0005_alter_user_last_login_null','2026-04-01 01:18:52.273873'),
(11,'auth','0006_require_contenttypes_0002','2026-04-01 01:18:52.275920'),
(12,'auth','0007_alter_validators_add_error_messages','2026-04-01 01:18:52.285667'),
(13,'auth','0008_alter_user_username_max_length','2026-04-01 01:18:52.314486'),
(14,'auth','0009_alter_user_last_name_max_length','2026-04-01 01:18:52.347580'),
(15,'auth','0010_alter_group_name_max_length','2026-04-01 01:18:52.378869'),
(16,'auth','0011_update_proxy_permissions','2026-04-01 01:18:52.392848'),
(17,'auth','0012_alter_user_first_name_max_length','2026-04-01 01:18:52.424169'),
(18,'core','0001_initial','2026-04-01 01:18:52.730310'),
(19,'core','0002_mesa_edad_preferencial_mesa_preferencial_and_more','2026-04-01 01:18:52.922616'),
(20,'core','0003_logopantalla','2026-04-01 01:18:52.945739'),
(21,'core','0004_marquesinapantalla','2026-04-01 01:18:52.961294'),
(22,'core','0005_configvideopantalla_videopantalla','2026-04-01 01:18:52.992644'),
(23,'core','0006_configapariencia','2026-04-01 01:18:53.010228'),
(24,'core','0007_alter_marquesinapantalla_options_and_more','2026-04-01 01:18:53.050536'),
(25,'core','0008_turno_motivo_preferencial_and_more','2026-04-01 01:18:53.114469'),
(26,'core','0009_configapariencia_pantalla_footer_texto','2026-04-01 01:18:53.157148'),
(27,'sessions','0001_initial','2026-04-01 01:18:53.196768');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES
('0wq2297horlc9x3jnzziwjdhui5c6qai','.eJxVjMsOwiAQRf-FtSFAebp07zeQGQakaiAp7cr479qkC93ec859sQjbWuM28hJnYmcm2el3Q0iP3HZAd2i3zlNv6zIj3xV-0MGvnfLzcrh_BxVG_dbJJZknZTCIbNGhAFTO6lD8BMZ6q0iYMFkA8EX6AOAKCV3IFqMzJM_eH-MQODw:1w7kMK:O4LMjsEk5YcTVQlCiYE_HDxkOoCdBpf8pzwM5tLk1pI','2026-04-15 01:27:04.804301');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Dumping routines for database 'totem_ia'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-04-01  8:04:41
