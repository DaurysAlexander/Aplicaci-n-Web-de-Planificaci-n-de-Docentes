-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-05-2024 a las 05:30:58
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `teacher_planner`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos_o_maquinarias`
--

CREATE TABLE `equipos_o_maquinarias` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Descripcion` varchar(255) NOT NULL,
  `Observacion` varchar(255) NOT NULL,
  `Fecha` date NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Solicitado_por` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `equipos_o_maquinarias`:
--   `user_id`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `equipos_o_maquinarias`
--

INSERT INTO `equipos_o_maquinarias` (`id`, `area_taller`, `Cantidad`, `Descripcion`, `Observacion`, `Fecha`, `Nombre`, `Solicitado_por`, `user_id`) VALUES
(272, 'Desarrolllo de Aplicaciones Informáticas', 10, 'nada', 'nada', '2024-05-28', 'Ercilio', 'Jose Rijo', 7),
(273, 'Desarrolllo de Aplicaciones Informáticas', 10, 'nada', 'nada', '2024-05-29', 'Ercilio', 'Jose Rijo', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `events`:
--   `user_id`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `events`
--

INSERT INTO `events` (`id`, `title`, `start_date`, `end_date`, `user_id`) VALUES
(27, 'hola', '2024-04-26', '2024-04-27', 7),
(28, 'Holaaaa', '2024-04-26', '2024-04-27', 7),
(29, 'Clase', '2024-04-26', '2024-04-27', 8),
(30, 'Lengua', '2024-04-26', '2024-04-27', 7),
(31, 'Clase de nada', '2024-04-27', '2024-04-28', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiales`
--

CREATE TABLE `materiales` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(255) DEFAULT NULL,
  `docente` varchar(255) DEFAULT NULL,
  `cantidad` text DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `en_existencia` text DEFAULT NULL,
  `comprar` text DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `client_email` varchar(100) NOT NULL,
  `client_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `materiales`:
--   `user_id`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `materiales`
--

INSERT INTO `materiales` (`id`, `area_taller`, `docente`, `cantidad`, `descripcion`, `en_existencia`, `comprar`, `user_id`, `client_email`, `client_name`) VALUES
(18, 'Desarrolllo de Aplicaciones Informáticas', 'Ercilio Alvarez', '20', 'Si muy buena', '50', '20', 7, '', ''),
(19, 'Prueba', 'Jhoneimy', '1000', 'xdddd', '100', '200', 9, '', ''),
(29, 'nada', 'Ercilio', '2', 'xdfeef3', '3', 'si', 7, '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planificaciones`
--

CREATE TABLE `planificaciones` (
  `id` int(11) NOT NULL,
  `institucion` text DEFAULT NULL,
  `taller` text DEFAULT NULL,
  `ra` text DEFAULT NULL,
  `elementos_capacidad` text DEFAULT NULL,
  `nivel` text DEFAULT NULL,
  `fecha` text DEFAULT NULL,
  `estrategias` text DEFAULT NULL,
  `actividades_evaluacion` text DEFAULT NULL,
  `contenidos_trabajados` text DEFAULT NULL,
  `docente` text DEFAULT NULL,
  `codigo` text DEFAULT NULL,
  `UC` text DEFAULT NULL,
  `inicio` date DEFAULT NULL,
  `termino` date DEFAULT NULL,
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `planificaciones`:
--   `id_user`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `planificaciones`
--

INSERT INTO `planificaciones` (`id`, `institucion`, `taller`, `ra`, `elementos_capacidad`, `nivel`, `fecha`, `estrategias`, `actividades_evaluacion`, `contenidos_trabajados`, `docente`, `codigo`, `UC`, `inicio`, `termino`, `id_user`) VALUES
(1, 'Instituto Politecnico Parroquial Santa Ana', 'Desarrolllo de Aplicaciones Informáticas', 'RA3.1 Aplicar procesos y  técnicas de prueba de la  aplicación o sistema  desarrollado para asegurar  su calidad y funcionalidad,  según el tipo de prueba  seleccionada.  VALORACION: 30 Puntos', 'EC3.1: Implementar  procesos y técnicas de  prueba de la aplicación o  el sistema desarrollado  para asegurar su calidad  y funcionalidad, según el  tipo de prueba  seleccionada.', 'Análisis Conocimiento Aplicación', 'Septiembre – Diciembre', 'CE3.1.1 Reconocer los  parámetros que rigen la  calidad de la organización.  CE3.1.2 Seleccionar el tipo de  prueba (de códigos, unitarias,  integración, sistemas,  aceptación, caja blanca y caja  negra) que se realizarán al  sistema.  CE3.1.3 En un supuesto  práctico, implementar la  prueba seleccionada de: - Códigos. - Unitarias. - Integración. - Sistemas. - Aceptación. - Caja blanca y  caja negra, cumpliendo los  criterios de calidad.', 'CR3.1.1 Reconoce los parámetros  que rigen la calidad de la organización.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.2 Selecciona el tipo de  pruebas (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra) que se  realizarán al sistema.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.3 Implementa la prueba  seleccionada (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra)  cumpliendo los criterios de  calidad. Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario.', 'Conceptuales: Técnicas de pruebas.   Gestión de la calidad.   Calidad de los servicios.   Medición de la calidad.  Conceptos, principios, niveles y sistema.   Pruebas y tipos. Procedimentales: Identificación de los parámetros de calidad de las  organizaciones públicas y privadas.  Identificación de las diferentes técnicas de prueba de  sistemas. Actitudinales: Valoración de normas de seguridad y prevención de riesgos  laborales.  Disposición al desarrollo de la capacidad de análisis y de  síntesis.  Valoración de la importancia que tiene en un sistema  informático la integridad y seguridad de los datos.  Valoración de los juicios emitidos por sus compañeros. Sensibilización por la consecución de un medio de  recopilación no contaminado.  Valoración de los instrumentos en la recopilación de  información', 'Jose Luis Rijo', 'MF_055_3', 'Aplicar los procesos de  prueba, implementación, mantenimiento preventivo y correctivo a las aplicaciones informáticas y sistemas desarrollados para garantizar el ciclo de vida de desarrollo de software.', '2024-04-16', '2024-04-30', 7),
(3, 'qhwduhwq', 'dqwwqdq', 'dsvdsv', 'vdsvdsvsb', 'bsfbdsb', 'bgdbgf', 'ngnfnfgm', 'ffwewfwe', 'wfewfwefe', 'dqdwqdqd', 'fdvsfvsv', 'vddsvds', '2024-04-16', '2024-04-17', 8),
(4, 'Instituto Politecnico Parroquial Santa Ana', 'Desarrolllo de Aplicaciones Informáticas', 'RA3.1 Aplicar procesos y  técnicas de prueba de la  aplicación o sistema  desarrollado para asegurar  su calidad y funcionalidad,  según el tipo de prueba  seleccionada.  VALORACION: 30 Puntos', 'EC3.1: Implementar  procesos y técnicas de  prueba de la aplicación o  el sistema desarrollado  para asegurar su calidad  y funcionalidad, según el  tipo de prueba  seleccionada.', 'Análisis Conocimiento Aplicación', 'Septiembre – Diciembre', 'CE3.1.1 Reconocer los  parámetros que rigen la  calidad de la organización.  CE3.1.2 Seleccionar el tipo de  prueba (de códigos, unitarias,  integración, sistemas,  aceptación, caja blanca y caja  negra) que se realizarán al  sistema.  CE3.1.3 En un supuesto  práctico, implementar la  prueba seleccionada de: - Códigos. - Unitarias. - Integración. - Sistemas. - Aceptación. - Caja blanca y  caja negra, cumpliendo los  criterios de calidad.', 'CR3.1.1 Reconoce los parámetros  que rigen la calidad de la organización.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.2 Selecciona el tipo de  pruebas (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra) que se  realizarán al sistema.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.3 Implementa la prueba  seleccionada (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra)  cumpliendo los criterios de  calidad. Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario.', 'Conceptuales: Técnicas de pruebas.   Gestión de la calidad.   Calidad de los servicios.   Medición de la calidad.  Conceptos, principios, niveles y sistema.   Pruebas y tipos. Procedimentales: Identificación de los parámetros de calidad de las  organizaciones públicas y privadas.  Identificación de las diferentes técnicas de prueba de  sistemas. Actitudinales: Valoración de normas de seguridad y prevención de riesgos  laborales.  Disposición al desarrollo de la capacidad de análisis y de  síntesis.  Valoración de la importancia que tiene en un sistema  informático la integridad y seguridad de los datos.  Valoración de los juicios emitidos por sus compañeros. Sensibilización por la consecución de un medio de  recopilación no contaminado.  Valoración de los instrumentos en la recopilación de  información', 'Natanel', 'MF_055_3', 'Aplicar los procesos de  prueba, implementación, mantenimiento preventivo y correctivo a las aplicaciones informáticas y sistemas desarrollados para garantizar el ciclo de vida de desarrollo de software.', '2024-04-18', '2024-04-30', 10),
(7, 'Instituto Politecnico Parroquial Santa Ana', 'Desarrolllo de Aplicaciones Informáticas', 'Naadaaaaa', 'EC3.1: Implementar  procesos y técnicas de  prueba de la aplicación o  el sistema desarrollado  para asegurar su calidad  y funcionalidad, según el  tipo de prueba  seleccionada.', 'Análisis Conocimiento Aplicación', 'Septiembre – Diciembre', 'CE3.1.1 Reconocer los  parámetros que rigen la  calidad de la organización.  CE3.1.2 Seleccionar el tipo de  prueba (de códigos, unitarias,  integración, sistemas,  aceptación, caja blanca y caja  negra) que se realizarán al  sistema.  CE3.1.3 En un supuesto  práctico, implementar la  prueba seleccionada de: - Códigos. - Unitarias. - Integración. - Sistemas. - Aceptación. - Caja blanca y  caja negra, cumpliendo los  criterios de calidad.', 'CR3.1.1 Reconoce los parámetros  que rigen la calidad de la organización.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.2 Selecciona el tipo de  pruebas (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra) que se  realizarán al sistema.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.3 Implementa la prueba  seleccionada (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra)  cumpliendo los criterios de  calidad. Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario.', 'Conceptuales: Técnicas de pruebas.   Gestión de la calidad.   Calidad de los servicios.   Medición de la calidad.  Conceptos, principios, niveles y sistema.   Pruebas y tipos. Procedimentales: Identificación de los parámetros de calidad de las  organizaciones públicas y privadas.  Identificación de las diferentes técnicas de prueba de  sistemas. Actitudinales: Valoración de normas de seguridad y prevención de riesgos  laborales.  Disposición al desarrollo de la capacidad de análisis y de  síntesis.  Valoración de la importancia que tiene en un sistema  informático la integridad y seguridad de los datos.  Valoración de los juicios emitidos por sus compañeros. Sensibilización por la consecución de un medio de  recopilación no contaminado.  Valoración de los instrumentos en la recopilación de  información', 'Natanel', 'MF_055_3', 'Aplicar los procesos de  prueba, implementación, mantenimiento preventivo y correctivo a las aplicaciones informáticas y sistemas desarrollados para garantizar el ciclo de vida de desarrollo de software.', '2024-04-28', '2024-04-30', 7),
(9, 'Instituto Politecnico Parroquial Santa Ana', 'Desarrolllo de Aplicaciones Informáticas', 'hjjnnj', 'EC3.1: Implementar  procesos y técnicas de  prueba de la aplicación o  el sistema desarrollado  para asegurar su calidad  y funcionalidad, según el  tipo de prueba  seleccionada.', 'Análisis Conocimiento Aplicación', 'Septiembre – Diciembre', 'CE3.1.1 Reconocer los  parámetros que rigen la  calidad de la organización.  CE3.1.2 Seleccionar el tipo de  prueba (de códigos, unitarias,  integración, sistemas,  aceptación, caja blanca y caja  negra) que se realizarán al  sistema.  CE3.1.3 En un supuesto  práctico, implementar la  prueba seleccionada de: - Códigos. - Unitarias. - Integración. - Sistemas. - Aceptación. - Caja blanca y  caja negra, cumpliendo los  criterios de calidad.', 'CR3.1.1 Reconoce los parámetros  que rigen la calidad de la organización.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.2 Selecciona el tipo de  pruebas (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra) que se  realizarán al sistema.  Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario. CR3.1.3 Implementa la prueba  seleccionada (códigos, unitarias,  integración, sistemas, aceptación,  caja blanca y caja negra)  cumpliendo los criterios de  calidad. Instrumento: Diagnostica con  Practica en el Computador.  Apuntes de Diario.', 'Conceptuales: Técnicas de pruebas.   Gestión de la calidad.   Calidad de los servicios.   Medición de la calidad.  Conceptos, principios, niveles y sistema.   Pruebas y tipos. Procedimentales: Identificación de los parámetros de calidad de las  organizaciones públicas y privadas.  Identificación de las diferentes técnicas de prueba de  sistemas. Actitudinales: Valoración de normas de seguridad y prevención de riesgos  laborales.  Disposición al desarrollo de la capacidad de análisis y de  síntesis.  Valoración de la importancia que tiene en un sistema  informático la integridad y seguridad de los datos.  Valoración de los juicios emitidos por sus compañeros. Sensibilización por la consecución de un medio de  recopilación no contaminado.  Valoración de los instrumentos en la recopilación de  información', 'Natanel', 'MF_055_3', 'Aplicar los procesos de  prueba, implementación, mantenimiento preventivo y correctivo a las aplicaciones informáticas y sistemas desarrollados para garantizar el ciclo de vida de desarrollo de software.', '2024-04-20', '2024-04-21', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planificacion_academica`
--

CREATE TABLE `planificacion_academica` (
  `id` int(11) NOT NULL,
  `instituto` text DEFAULT NULL,
  `asignatura` text DEFAULT NULL,
  `grado` text DEFAULT NULL,
  `docente` text DEFAULT NULL,
  `tiempo_asignado` text DEFAULT NULL,
  `tema` text DEFAULT NULL,
  `competencias_fundamentales` text DEFAULT NULL,
  `nivel_de_dominio` text DEFAULT NULL,
  `competencias_especificas` text DEFAULT NULL,
  `situacion_de_aprendizaje` text DEFAULT NULL,
  `secuencias_didacticas` text DEFAULT NULL,
  `momento` text DEFAULT NULL,
  `tiempo` text DEFAULT NULL,
  `actividades_de_aprendizaje` text DEFAULT NULL,
  `indicadores_de_logro` text DEFAULT NULL,
  `metacognicion` text DEFAULT NULL,
  `evidencias` text DEFAULT NULL,
  `tecnicas_e_instrumentos` text DEFAULT NULL,
  `recursos` text DEFAULT NULL,
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `planificacion_academica`:
--   `id_user`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `planificacion_academica`
--

INSERT INTO `planificacion_academica` (`id`, `instituto`, `asignatura`, `grado`, `docente`, `tiempo_asignado`, `tema`, `competencias_fundamentales`, `nivel_de_dominio`, `competencias_especificas`, `situacion_de_aprendizaje`, `secuencias_didacticas`, `momento`, `tiempo`, `actividades_de_aprendizaje`, `indicadores_de_logro`, `metacognicion`, `evidencias`, `tecnicas_e_instrumentos`, `recursos`, `id_user`) VALUES
(1, 'Instituto Politecnico Parroquial Santa Ana', 'Lengua Española', '5to F', 'Ercilio Alvarez', '3 horas', 'Nada', 'Nada', 'Nada', 'Nada', 'Nadaa', 'Nadaa', 'Nadaa', 'Nadaa', 'Nadaaaaa', 'Nadaaaaaaa', 'Nadaaaaa', 'Nadaaaa', 'Nadaaaa', 'Nadaaaa', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas_limpieza`
--

CREATE TABLE `practicas_limpieza` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(50) DEFAULT NULL,
  `Cantidad` int(255) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `Observacion` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Solicitado_por` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `practicas_limpieza`:
--   `user_id`
--       `users` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas_murales`
--

CREATE TABLE `practicas_murales` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(50) DEFAULT NULL,
  `Cantidad` int(255) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `Observacion` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Solicitado_por` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `practicas_murales`:
--   `user_id`
--       `users` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas_oficina`
--

CREATE TABLE `practicas_oficina` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(50) DEFAULT NULL,
  `Cantidad` int(255) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `Observacion` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Solicitado_por` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `practicas_oficina`:
--   `user_id`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `practicas_oficina`
--

INSERT INTO `practicas_oficina` (`id`, `area_taller`, `Cantidad`, `Descripcion`, `Observacion`, `Fecha`, `Nombre`, `Solicitado_por`, `user_id`) VALUES
(1, 'Desarrollo', 20, 'vvgvgvg', 'ggvgvg', '0000-00-00', NULL, NULL, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas_pedagogicas`
--

CREATE TABLE `practicas_pedagogicas` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(50) DEFAULT NULL,
  `Cantidad` int(255) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `Observacion` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Solicitado_por` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `practicas_pedagogicas`:
--   `user_id`
--       `users` -> `id`
--

--
-- Volcado de datos para la tabla `practicas_pedagogicas`
--

INSERT INTO `practicas_pedagogicas` (`id`, `area_taller`, `Cantidad`, `Descripcion`, `Observacion`, `Fecha`, `Nombre`, `Solicitado_por`, `user_id`) VALUES
(1, 'Desarrollo', 20, 'vvgvgvg', 'ggvgvg', '0000-00-00', NULL, NULL, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas_reparaciones`
--

CREATE TABLE `practicas_reparaciones` (
  `id` int(11) NOT NULL,
  `area_taller` varchar(50) DEFAULT NULL,
  `Cantidad` int(11) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `Observacion` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Solicitado_por` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `practicas_reparaciones`:
--   `user_id`
--       `users` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `requerimientos`
--

CREATE TABLE `requerimientos` (
  `id` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Descripcion` text NOT NULL,
  `Observacion` text NOT NULL,
  `Fecha` date NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Solicitado_por` varchar(50) NOT NULL,
  `Equipos_o_Maquinarias` int(11) DEFAULT NULL,
  `Practicas_Pedagogicas` int(11) DEFAULT NULL,
  `Materiales_Oficina` int(11) DEFAULT NULL,
  `Murales_o_Actividades` int(11) DEFAULT NULL,
  `Materiales_Limpieza` int(11) DEFAULT NULL,
  `Reparaciones_Internas` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `requerimientos`:
--   `user_id`
--       `users` -> `id`
--   `Equipos_o_Maquinarias`
--       `equipos_o_maquinarias` -> `id`
--   `Practicas_Pedagogicas`
--       `practicas_pedagogicas` -> `id`
--   `Murales_o_Actividades`
--       `practicas_murales` -> `id`
--   `Materiales_Oficina`
--       `practicas_oficina` -> `id`
--   `Reparaciones_Internas`
--       `practicas_reparaciones` -> `id`
--   `Materiales_Limpieza`
--       `practicas_limpieza` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `roles`:
--

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'Administradores'),
(2, 'Gestiones'),
(3, 'Docentes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `role` int(11) NOT NULL,
  `foto_perfil` blob NOT NULL,
  `nombre_apellido` varchar(225) NOT NULL,
  `edad` int(100) NOT NULL,
  `pais` varchar(255) NOT NULL,
  `telefono` int(30) NOT NULL,
  `materia` varchar(255) NOT NULL,
  `Instituto` varchar(100) NOT NULL,
  `Taller` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- RELACIONES PARA LA TABLA `users`:
--   `role`
--       `roles` -> `id`
--

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `foto_perfil`, `nombre_apellido`, `edad`, `pais`, `telefono`, `materia`, `Instituto`, `Taller`) VALUES
(4, 'Miguel', 'elmiguel', 2, '', 'juan martinez', 57, 'albania', 2147483647, 'tu mama', '', ''),
(5, 'Policarpioo', 'hellopolicarpio', 1, '', '', 0, '', 0, '', '', ''),
(6, 'Geison', 'hellocotto', 2, '', '', 0, '', 0, '', '', ''),
(7, 'Ercilio', 'hola121621', 3, '', 'Ercilio Alvarez', 40, 'República Dominicana', 2147483647, 'Ofimatica', '', ''),
(8, 'Eury Samuel', 'eurysamuel', 3, '', '', 0, '', 0, '', '', ''),
(9, 'jhoneimy', '12345678', 3, '', 'Jhoneimy Batista', 17, 'República Dominicana', 8767868, 'Prueba', '', ''),
(10, 'Natanael_18', 'nigga12345', 3, '', '', 0, '', 0, '', '', ''),
(14, 'Prueba1', '12345678', 3, '', '', 0, '', 0, '', '', ''),
(15, 'ariannyg', '123456789', 3, '', '', 0, '', 0, '', '', '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `equipos_o_maquinarias`
--
ALTER TABLE `equipos_o_maquinarias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `materiales`
--
ALTER TABLE `materiales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `user_id_2` (`user_id`);

--
-- Indices de la tabla `planificaciones`
--
ALTER TABLE `planificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`id_user`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `planificacion_academica`
--
ALTER TABLE `planificacion_academica`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `practicas_limpieza`
--
ALTER TABLE `practicas_limpieza`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `practicas_murales`
--
ALTER TABLE `practicas_murales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `practicas_oficina`
--
ALTER TABLE `practicas_oficina`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `practicas_pedagogicas`
--
ALTER TABLE `practicas_pedagogicas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `practicas_reparaciones`
--
ALTER TABLE `practicas_reparaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `requerimientos`
--
ALTER TABLE `requerimientos`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Equipos_o_Maquinarias` (`Equipos_o_Maquinarias`,`Practicas_Pedagogicas`,`Materiales_Oficina`,`Murales_o_Actividades`,`Materiales_Limpieza`,`Reparaciones_Internas`),
  ADD KEY `Practicas_Pedagogicas` (`Practicas_Pedagogicas`),
  ADD KEY `Murales_o_Actividades` (`Murales_o_Actividades`),
  ADD KEY `Materiales_Oficina` (`Materiales_Oficina`),
  ADD KEY `Reparaciones_Internas` (`Reparaciones_Internas`),
  ADD KEY `Materiales_Limpieza` (`Materiales_Limpieza`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role` (`role`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `equipos_o_maquinarias`
--
ALTER TABLE `equipos_o_maquinarias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=275;

--
-- AUTO_INCREMENT de la tabla `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `materiales`
--
ALTER TABLE `materiales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `planificaciones`
--
ALTER TABLE `planificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `planificacion_academica`
--
ALTER TABLE `planificacion_academica`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `practicas_limpieza`
--
ALTER TABLE `practicas_limpieza`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `practicas_murales`
--
ALTER TABLE `practicas_murales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `practicas_oficina`
--
ALTER TABLE `practicas_oficina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `practicas_pedagogicas`
--
ALTER TABLE `practicas_pedagogicas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `practicas_reparaciones`
--
ALTER TABLE `practicas_reparaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `equipos_o_maquinarias`
--
ALTER TABLE `equipos_o_maquinarias`
  ADD CONSTRAINT `equipos_o_maquinarias_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `materiales`
--
ALTER TABLE `materiales`
  ADD CONSTRAINT `materiales_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `planificaciones`
--
ALTER TABLE `planificaciones`
  ADD CONSTRAINT `planificaciones_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `planificacion_academica`
--
ALTER TABLE `planificacion_academica`
  ADD CONSTRAINT `planificacion_academica_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `practicas_limpieza`
--
ALTER TABLE `practicas_limpieza`
  ADD CONSTRAINT `practicas_limpieza_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `practicas_murales`
--
ALTER TABLE `practicas_murales`
  ADD CONSTRAINT `practicas_murales_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `practicas_oficina`
--
ALTER TABLE `practicas_oficina`
  ADD CONSTRAINT `practicas_oficina_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `practicas_pedagogicas`
--
ALTER TABLE `practicas_pedagogicas`
  ADD CONSTRAINT `practicas_pedagogicas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `practicas_reparaciones`
--
ALTER TABLE `practicas_reparaciones`
  ADD CONSTRAINT `practicas_reparaciones_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `requerimientos`
--
ALTER TABLE `requerimientos`
  ADD CONSTRAINT `requerimientos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_2` FOREIGN KEY (`Equipos_o_Maquinarias`) REFERENCES `equipos_o_maquinarias` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_3` FOREIGN KEY (`Practicas_Pedagogicas`) REFERENCES `practicas_pedagogicas` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_4` FOREIGN KEY (`Murales_o_Actividades`) REFERENCES `practicas_murales` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_5` FOREIGN KEY (`Materiales_Oficina`) REFERENCES `practicas_oficina` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_6` FOREIGN KEY (`Reparaciones_Internas`) REFERENCES `practicas_reparaciones` (`id`),
  ADD CONSTRAINT `requerimientos_ibfk_7` FOREIGN KEY (`Materiales_Limpieza`) REFERENCES `practicas_limpieza` (`id`);

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
