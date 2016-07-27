Hash
======

hash length extension
-----

SHA-1 , SHA-256 , MD-5

ไว้เวลา inject แล้วมี MAC โดยจะใช้ขยายข้อความออกไปโดยที่ไม่ต้องรู้ salt เลย
เช่น
original : `count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo`
desired : `count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo&waffle=liege`

เมื่อรู้ hash ของ salt+original แล้ว จะรู้ hash ของ `count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x28&waffle=liege`

