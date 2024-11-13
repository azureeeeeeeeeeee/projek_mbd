-- DB TABLE SETUP

-- USERS TABLE
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIPE_KENDARAAN TABLE
CREATE TABLE tipe_kendaraan (
    id INT PRIMARY KEY,
    tipe VARCHAR(50) UNIQUE NOT NULL
);

-- KENDARAAN TABLE
CREATE TABLE kendaraan (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plat_nomor VARCHAR(50) UNIQUE NOT NULL,
    tersedia BOOLEAN DEFAULT TRUE,
    harga DECIMAL(10, 2) NOT NULL,
    tipe INT NOT NULL,
    
    FOREIGN KEY (tipe) REFERENCES tipe_kendaraan(id)
);

-- METODE_PEMBAYARAN TABLE
CREATE TABLE metode_pembayaran (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(20) NOT NULL
)

-- SEWA TABLE
CREATE TABLE sewa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_kendaraan INT NOT NULL,
    id_pelanggan INT NOT NULL,
    tanggal_mulai DATE NOT NULL,
    tanggal_selesai DATE NOT NULL,
    rusak BOOLEAN,
    tanggal_kembali DATE,
    biaya_denda DECIMAL(10, 2),
    total_bayar DECIMAL(10, 2),
    metode_pembayaran INT,
    
    FOREIGN KEY (id_kendaraan) REFERENCES kendaraan(id),
    FOREIGN KEY (id_pelanggan) REFERENCES users(id),
    FOREIGN KEY (metode_pembayaran) REFERENCES metode_pembayaran(id)
);




-- STORED FUNCTION SETUP
DELIMITER //

-- get or create tipe kendaraan berdasarkan input
DROP FUNCTION IF EXISTS get_or_create_tipe_kendaraan //
CREATE FUNCTION get_or_create_tipe_kendaraan(tipe_input VARCHAR(50)) 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE tipe_id INT;

    SELECT id INTO tipe_id 
    FROM tipe_kendaraan 
    WHERE tipe = tipe_input
    LIMIT 1;

    IF tipe_id IS NULL THEN
        INSERT INTO tipe_kendaraan (tipe) 
        VALUES (tipe_input);
        
        SELECT LAST_INSERT_ID() INTO tipe_id;
    END IF;

    RETURN tipe_id;
END //


-- get or create metode pembayaran berdasarkan user input
DROP FUNCTION IF EXISTS get_or_create_metode_pembayaran //
CREATE FUNCTION get_or_create_metode_pembayaran(nama_input VARCHAR(20)) 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE metode_id INT;

    SELECT id INTO metode_id 
    FROM metode_pembayaran 
    WHERE nama = nama_input
    LIMIT 1;

    IF metode_id IS NULL THEN
        INSERT INTO metode_pembayaran (nama) 
        VALUES (nama_input);
        
        SELECT LAST_INSERT_ID() INTO metode_id;
    END IF;

    RETURN metode_id;
END //


-- fetch id kendaraan berdasarkan plat nomor
DROP FUNCTION IF EXISTS get_kendaraan_by_plat_nomor //
CREATE FUNCTION get_kendaraan_by_plat_nomor(plat_nomor_input VARCHAR(50)) 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE kendaraan_id INT;

    SELECT id INTO kendaraan_id 
    FROM kendaraan 
    WHERE plat_nomor = plat_nomor_input
    LIMIT 1;

    RETURN kendaraan_id;
END //




-- GET TOTAL REVENUE (KENDARAAN)
DROP FUNCTION IF EXISTS get_total_revenue_by_kendaraan //

CREATE FUNCTION get_total_revenue_by_kendaraan(
    plat_nomor_input VARCHAR(50)
)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total_revenue DECIMAL(10, 2);

    DECLARE id_kendaraan_input INT;
    SET id_kendaraan_input = get_kendaraan_by_plat_nomor(plat_nomor_input);

    IF id_kendaraan_input IS NULL THEN
        RETURN 0;
    END IF;

    SELECT IFNULL(SUM(total_bayar), 0) INTO total_revenue
    FROM sewa
    WHERE id_kendaraan = id_kendaraan_input;

    RETURN total_revenue;
END //


-- GET TOTAL REVENUE (USER)
CREATE FUNCTION get_total_revenue_by_user(
    id_pelanggan_input INT
)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total_spending DECIMAL(10, 2);

    SELECT IFNULL(SUM(total_bayar), 0) INTO total_spending
    FROM sewa
    WHERE id_pelanggan = id_pelanggan_input;

    RETURN total_spending;
END //

DELIMITER ;




-- STORED PROCEDURE SETUP
DELIMITER //

-- Fetch user from db
CREATE PROCEDURE get_user(IN in_email VARCHAR(50))
BEGIN
	START TRANSACTION;
    SELECT id, username, password, is_admin
    FROM users
    WHERE username = in_email;
    COMMIT;
END //

-- Create new user
CREATE PROCEDURE create_user(
    IN in_email VARCHAR(50),
    IN in_fullname VARCHAR(100),
    IN in_password VARCHAR(255),
    IN in_is_admin BOOLEAN
)
BEGIN
	START TRANSACTION;
    INSERT INTO users (email, fullname, password, is_admin)
    VALUES (in_email, in_fullname, in_password, in_is_admin);
    COMMIT;
END //

-- Tambah kendaraan baru
DROP PROCEDURE IF EXISTS tambah_kendaraan //
CREATE PROCEDURE tambah_kendaraan(
    IN plat_nomor_input VARCHAR(50),
    IN harga_input DECIMAL(10, 2),
    IN tipe_input VARCHAR(50)
)
BEGIN
    DECLARE tipe_id INT;

    SET tipe_id = get_or_crate_tipe_kendaraan(tipe_input);
    
    START TRANSACTION;
    INSERT INTO kendaraan (plat_nomor, harga, tipe)
    VALUES (plat_nomor_input, harga_input, tipe_id);
    COMMIT;
END //

-- Hapus kendaraan
DROP PROCEDURE IF EXISTS hapus_kendaraan //
CREATE PROCEDURE hapus_kendaraan(
    IN plat_nomor_input VARCHAR(50)
)
BEGIN
	START TRANSACTION;
    DELETE FROM kendaraan 
    WHERE plat_nomor = plat_nomor_input;
    COMMIT;
END //




-- Sewa kendaraan
DROP PROCEDURE IF EXISTS sewa_kendaraan //
CREATE PROCEDURE sewa_kendaraan(
    IN plat_nomor_input VARCHAR(50),
    IN id_pelanggan_input INT,
    IN tanggal_mulai_input DATE,
    IN tanggal_selesai_input DATE
)
BEGIN
    DECLARE id_kendaraan_input INT;
    DECLARE harga_kendaraan DECIMAL(10, 2);
    DECLARE total_hari INT;
    DECLARE total_bayar DECIMAL(10, 2);
    DECLARE kendaraan_tersedia BOOLEAN;

    SET id_kendaraan_input = 	get_kendaraan_by_plat_nomor(plat_nomor_input);

    IF id_kendaraan_input IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Kendaraan tidak ditemukan.';
    END IF;
	
    SELECT tersedia INTO kendaraan_tersedia
    FROM kendaraan
    WHERE id = id_kendaraan_input;

    IF NOT kendaraan_tersedia THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Kendaraan tidak tersedia untuk periode sewa ini.';
    END IF;

    SELECT harga INTO harga_kendaraan
    FROM kendaraan
    WHERE id = id_kendaraan_input;

    SET total_hari = DATEDIFF(tanggal_selesai_input, tanggal_mulai_input);

    SET total_bayar = harga_kendaraan * total_hari;

	START TRANSACTION;
    INSERT INTO sewa (
        id_kendaraan, 
        id_pelanggan, 
        tanggal_mulai, 
        tanggal_selesai, 
        total_bayar
    )
    VALUES (
        id_kendaraan_input, 
        id_pelanggan_input, 
        tanggal_mulai_input, 
        tanggal_selesai_input, 
        total_bayar
    );

    UPDATE kendaraan
    SET tersedia = FALSE
    WHERE id = id_kendaraan_input;
    
    COMMIT;

END //





-- Kembalikan kendaraan
DROP PROCEDURE IF EXISTS kembalikan_kendaraan //

CREATE PROCEDURE kembalikan_kendaraan(
    IN plat_nomor_input VARCHAR(50),
    IN tanggal_kembali_input DATE,
    IN rusak_input BOOLEAN,
    IN metode_pembayaran_input VARCHAR(50)
)
BEGIN
    DECLARE id_kendaraan_input INT;
    DECLARE harga_kendaraan DECIMAL(10, 2);
    DECLARE tanggal_sewa_mulai DATE;
    DECLARE tanggal_sewa_selesai DATE;
    DECLARE total_bayar DECIMAL(10, 2);
    DECLARE biaya_denda DECIMAL(10, 2);
    DECLARE total_hari INT;
    DECLARE total_hari_terlambat INT;
    DECLARE sewa_id INT;
    DECLARE metode_pembayaran_id INT;

    SET id_kendaraan_input = get_kendaraan_by_plat_nomor(plat_nomor_input);

    IF id_kendaraan_input IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Kendaraan tidak ditemukan.';
    END IF;

    SELECT id, tanggal_mulai, tanggal_selesai INTO sewa_id, tanggal_sewa_mulai, tanggal_sewa_selesai
    FROM sewa
    WHERE id_kendaraan = id_kendaraan_input AND tanggal_kembali IS NULL;

    IF tanggal_sewa_mulai IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sewa kendaraan tidak ditemukan.';
    END IF;

    SELECT harga INTO harga_kendaraan
    FROM kendaraan
    WHERE id = id_kendaraan_input;

    SET total_hari_terlambat = DATEDIFF(tanggal_kembali_input, tanggal_sewa_selesai);

    IF total_hari_terlambat > 0 THEN
        SET biaya_denda = total_hari_terlambat * 50000;
    ELSE
        SET biaya_denda = 0;
    END IF;

    IF rusak_input THEN
        SET biaya_denda = biaya_denda + 100000;
    END IF;

    SET total_hari = DATEDIFF(tanggal_sewa_selesai, tanggal_sewa_mulai);

    SET total_bayar = (harga_kendaraan * total_hari) + biaya_denda;

    SET metode_pembayaran_id = get_or_create_metode_pembayaran(metode_pembayaran_input);
    
    START TRANSACTION;
    UPDATE sewa
    SET tanggal_kembali = tanggal_kembali_input, 
        total_bayar = total_bayar, 
        biaya_denda = biaya_denda, 
        metode_pembayaran = metode_pembayaran_id, 
        rusak = rusak_input
    WHERE id = sewa_id;

    UPDATE kendaraan
    SET tersedia = TRUE
    WHERE id = id_kendaraan_input;
    COMMIT;

END //




-- GET SEWA HISTORY (Kendaraan)
DROP PROCEDURE IF EXISTS get_sewa_history_kendaraan //

CREATE PROCEDURE get_sewa_history_kendaraan(
    IN plat_nomor_input VARCHAR(50)
)
BEGIN
    DECLARE id_kendaraan_input INT;

    SET id_kendaraan_input = get_kendaraan_by_plat_nomor(plat_nomor_input);

    IF id_kendaraan_input IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Kendaraan tidak ditemukan.';
    END IF;

    SELECT 
        s.id AS sewa_id,
        s.id_kendaraan,
        k.plat_nomor,
        s.id_pelanggan,
        s.tanggal_mulai,
        s.tanggal_selesai,
        s.tanggal_kembali,
        s.total_bayar,
        s.biaya_denda,
        m.nama as metode_pembayaran,
        s.rusak
    FROM 
        sewa s
    JOIN 
        kendaraan k ON s.id_kendaraan = k.id
    LEFT JOIN 
        metode_pembayaran m ON s.metode_pembayaran = m.id
    WHERE 
        k.plat_nomor = plat_nomor_input
    ORDER BY 
        s.tanggal_mulai DESC;

END //


-- GET SEWA HISTORY (User)
DROP PROCEDURE IF EXISTS get_sewa_history_user //

CREATE PROCEDURE get_sewa_history_user(
    IN id_pelanggan_input INT
)
BEGIN

    SELECT 
        k.plat_nomor,
        s.tanggal_mulai,
        s.tanggal_selesai,
        s.rusak,
        s.total_bayar,
        m.nama
    FROM 
        sewa s
    JOIN 
        kendaraan k ON s.id_kendaraan = k.id
    LEFT JOIN 
        metode_pembayaran m ON s.metode_pembayaran = m.id
    WHERE 
        s.id_pelanggan = id_pelanggan_input
    ORDER BY 
        s.tanggal_mulai DESC;

END //



DELIMITER ;




-- USAGE

-- CALL get_sewa_history_kendaraan('KU 2713 GI')
-- CALL get_sewa_history_user(3)

-- CALL sewa_kendaraan('KU 2713 GI', 3, '2024-11-20', '2024-11-25')
-- CALL kembalikan_kendaraan('KU 2713 GI', '2024-11-25', FALSE, 'cash')

-- SELECT get_total_revenue_by_user(3)
-- SELECT get_total_revenue_by_kendaraan('KU 2713 GI')