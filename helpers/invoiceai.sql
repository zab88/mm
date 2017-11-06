-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 16, 2017 at 04:27 PM
-- Server version: 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `invoiceai`
--

-- --------------------------------------------------------

--
-- Table structure for table `invoice_doc_train`
--

CREATE TABLE `invoice_doc_train` (
  `id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIONS FOR TABLE `invoice_doc_train`:
--

-- --------------------------------------------------------

--
-- Table structure for table `invoice_fields_train`
--

CREATE TABLE `invoice_fields_train` (
  `id` int(11) NOT NULL,
  `invoice_train_id` int(11) NOT NULL,
  `name` varchar(127) NOT NULL,
  `value` varchar(127) DEFAULT NULL,
  `use_or_not` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIONS FOR TABLE `invoice_fields_train`:
--   `invoice_train_id`
--       `invoice_doc_train` -> `id`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `invoice_doc_train`
--
ALTER TABLE `invoice_doc_train`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `invoice_fields_train`
--
ALTER TABLE `invoice_fields_train`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `invoice_doc_train`
--
ALTER TABLE `invoice_doc_train`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `invoice_fields_train`
--
ALTER TABLE `invoice_fields_train`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;