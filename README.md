# ThaiGov V2 Corpus

## English
- Data from Thai government website. https://www.thaigov.go.th
- This part of PyThaiNLP Project.
- Compiled by Mr.Wannaphong Phatthiyaphaibun
- License Dataset is public domain.

## Data format

- 1 file, 1 news, which is extracted from 1 url.

```
topic
(Blank line)
content
content
content
content
content
(Blank line)
ที่มา (URL source) : http://www.thaigov.go.th/news/contents/details/NNN
```

## Thai
- เป็นข้อมูลที่รวบรวมข่าวสารจากเว็บไซต์รัฐบาลไทย https://www.thaigov.go.th
- โครงการนี้เป็นส่วนหนึ่งในแผนพัฒนา [PyThaiNLP](https://github.com/PyThaiNLP/)
- รวบรวมโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
- ข้อมูลที่รวบรวมในคลังข้อความนี้เป็นสาธารณสมบัติ (public domain) ตามพ.ร.บ.ลิขสิทธิ์ พ.ศ. 2537 มาตรา 7 (สิ่งต่อไปนี้ไม่ถือว่าเป็นงานอันมีลิขสิทธิ์ตามพระราชบัญญัตินี้ (1) ข่าวประจำวัน และข้อเท็จจริงต่างๆ ที่มีลักษณะเป็นเพียงข่าวสารอันมิใช่งานในแผนกวรรณคดี แผนกวิทยาศาสตร์ หรือแผนกศิลปะ [...] (3) ระเบียบ ข้อบังคับ ประกาศ คำสั่ง คำชี้แจง และหนังสือตอบโต้ของกระทรวง ทบวง กรม หรือหน่วยงานอื่นใดของรัฐหรือของท้องถิ่น [...])

**สามารถติดตามประวัติการแก้ไขคลังข้อความนี้ได้ผ่านระบบ Git**

### จำนวนข่าว

- วันเริ่มต้นโครงการ 17 ก.ย. 2563

### รูปแบบข้อมูล

- 1 ไฟล์ 1 ข่าว ซึ่งดึงมาจาก 1 url

```
หัวเรื่อง
(บรรทัดว่าง)
เนื้อความ
เนื้อความ
เนื้อความ
เนื้อความ
เนื้อความ
(บรรทัดว่าง)
ที่มา : http://www.thaigov.go.th/news/contents/details/NNN
```

### รายละเอียดชื่อไฟล์

- ชื่อหมวดหมู่_จำนวนที่ของข่าว.txt

### Script

- run.py สำหรับเก็บข้อมูลจากหน้าเว็บ โดยจะดึงหน้าเว็บจาก url ```http://www.thaigov.go.th/news/contents/details/NNN``` โดยที่ NNN คือเลขจำนวนเต็ม
    - เปลี่ยนค่าตัวแปร i ในไฟล์เป็นเลขที่ต้องการเริ่มเก็บ
- clean.py สำหรับทำความสะอาดข้อมูลเบื้องต้น โดยจะลบช่องว่างหน้าและท้ายบรรทัด ลบบรรทัดว่าง
    - ```clean.py ชื่อไฟล์```
    - ```clean.py ชื่อไฟล์1 ชื่อไฟล์2```
    - ```clean.py *.txt```



We build Thai NLP.

PyThaiNLP
