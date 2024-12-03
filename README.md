# Sewa Kendaraan

REST API berbasis Flask untuk manajemen sewa kendaraan.

### History

History User, { email: email (optional) }

```
POST /history/user/
```

History Kendaraan, { plat_nomor: string }

```
POST /history/kendaraan/
```

### User dan Auth

Login, { name: email, password: string }

```
POST /auth/login/
```

Logout,
```
POST /auth/logout/
```

Registrasi User, { fullname: string, email: email, password: string }

```
POST /users/user
```

Registrasi Admin, { fullname: string, email: email, password: string }

```
POST /users/admin
```

Delete User, { email: email }

```
DELETE /users/
```

Fetch semua user,

```
GET /users/
```

### Kendaraan

Tambah Kendaraan, { plat_nomor: string, harga_per_hari: int, tipe: string }

```
POST /kendaraan/
```

Hapus Kendaraan, { plat_nomor: string }

```
DELETE /kendaraan/
```

Update Kendaraan, { plat_nomor: string, harga_baru: int }

```
PUT /kendaraan/
```

Fetch semua kendaraan,

```
GET /kendaraan/
```

### Sewa

Sewa Kendaraan, { plat_nomor: string, tanggal_mulai: date, tanggal_selesai: date }

```
POST /sewa/
```

Fetch semua data sewa,

```
GET /sewa/
```

Hapus Data Sewa,

```
DELETE /sewa/<id>
```

Kembalikan kendaraan, { plat_nomor: string, tanggal_kembali: date, rusak: boolean, metode_pembayaran: string }

```
GET /kembali/
```

### Tipe Kendaraan

Fetch semua tipe kendaraan,

```
GET /kendaraan/tipe/
```

Hapus Tipe Kendaraan, { tipe: string }

```
DELETE /kendaraan/tipe/
```
