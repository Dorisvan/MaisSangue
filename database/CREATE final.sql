-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Doacaodb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Doacaodb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Doacaodb` DEFAULT CHARACTER SET utf8 ;
USE `Doacaodb` ;

-- -----------------------------------------------------
-- Table `Doacaodb`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Doacaodb`.`Usuario` (
  `cpf` VARCHAR(25) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `idade` INT NOT NULL,
  `peso` VARCHAR(10) NOT NULL,
  `tipo_sanguineo` VARCHAR(10) NOT NULL,
  `cep` VARCHAR(30) NOT NULL,
  `cidade` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `telefone` VARCHAR(25) NULL,
  `opcao_doacao` VARCHAR(10) NULL,
  `estado_doacao` VARCHAR(20) NULL,
  `nivel_usuario` INT NULL,
  `estado_sessao` INT NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Doacaodb`.`Solicitacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Doacaodb`.`Solicitacao` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `data` DATE NOT NULL,
  `urgencia` INT NOT NULL,
  `local_internacao` VARCHAR(200) NOT NULL,
  `situacao` VARCHAR(45) NOT NULL,
  `Usuario_cpf` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Solicitacao_Usuario1_idx` (`Usuario_cpf` ASC),
  CONSTRAINT `fk_Solicitacao_Usuario1`
    FOREIGN KEY (`Usuario_cpf`)
    REFERENCES `Doacaodb`.`Usuario` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Doacaodb`.`Doacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Doacaodb`.`Doacao` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `data` DATE NOT NULL,
  `local_destino` VARCHAR(200) NOT NULL,
  `Usuario_cpf` VARCHAR(25) NOT NULL,
  `Solicitacao_codigo` BIGINT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Doacao_Usuario1_idx` (`Usuario_cpf` ASC),
  INDEX `fk_Doacao_Solicitacao1_idx` (`Solicitacao_codigo` ASC),
  CONSTRAINT `fk_Doacao_Usuario1`
    FOREIGN KEY (`Usuario_cpf`)
    REFERENCES `Doacaodb`.`Usuario` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Doacao_Solicitacao1`
    FOREIGN KEY (`Solicitacao_codigo`)
    REFERENCES `Doacaodb`.`Solicitacao` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Doacaodb`.`Doenca`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Doacaodb`.`Doenca` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Doacaodb`.`UsuarioDoenca`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Doacaodb`.`UsuarioDoenca` (
  `Doenca_id` BIGINT NOT NULL,
  `Usuario_cpf` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`Doenca_id`, `Usuario_cpf`),
  INDEX `fk_Doenca_has_Usuario_Usuario1_idx` (`Usuario_cpf` ASC),
  INDEX `fk_Doenca_has_Usuario_Doenca1_idx` (`Doenca_id` ASC),
  CONSTRAINT `fk_Doenca_has_Usuario_Doenca1`
    FOREIGN KEY (`Doenca_id`)
    REFERENCES `Doacaodb`.`Doenca` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Doenca_has_Usuario_Usuario1`
    FOREIGN KEY (`Usuario_cpf`)
    REFERENCES `Doacaodb`.`Usuario` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
