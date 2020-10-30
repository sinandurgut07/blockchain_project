# blockchain_project

Bu uygulama SDÜ Lisansüstü Blockchain dersi için geliştirilmiştir.
İşleyişi https://youtu.be/_8WTI0Nide8 linkinde anlatılmıştır.

Dosya onayı isteyen bir kullanıcı dosyayı ve onaylaması gereken kişileri seçip onaya göndermektedir. Onay süreci blockchain ile saklanmaktadır.
Kayıtta herhangibir değişiklik olması durumunda kanıt olarak blockchain yapısı kullanılacaktır. Onay sürecinin güvenilirliğini sağlamak hedeflenmiştir. 

Proje 2 aşamadan oluşmaktadır. 
1. Kullanıcı Tarafı(Client Side - 8069 portu kullanılmalıdır)

Bu tarafta Odoo frameworkü ile bir modül geliştirilmiştir. 
"res.users(kullanıcıların bulunduğu tablo)" tablosu genişletilmiş ve kullanıcılara one2many bir tablo aracılığıyla public ve private keyler oluşturulması sağlanmıştır. Burada RSA algoritması kullanılmıştır.
Geliştirilen modülde videoda da görüleceği gibi kullanıcı arayüzleri ayarlanmıştır. Kullanıcı dosyayı ekleyip onaylayacak kişileri seçmektedir. Ardından onaya göndermektedir.
Onay sürgüsündeki kişiler onayla yada rededetme işlemi yaptıklarında Madenci Bekleniyor statüsüne gelmektedir. Burada blockchain yapısının ilgili kayıtları mine etmesi beklenmektedir.

Çalıştırmak için odoo frameworkü kurulmalı ve konfigrasyon dosyasındaki addons klasörleri arasına "odoo_addon" dosyası verilmelidir. Bunun ardından odoo içerisinde app kısmından modülü yüklemek yeterlidir. Admin kullanıcısına gerekli yetkiler verilecek şekilde ayarlanmıştır. 

2. Blockchain yapısı:(5000 portu kullanılmalıdır.)
https://github.com/adilmoujahid/blockchain-python-tutorial 
Yukarıdaki linkteki uygulama yeni kurguya göre düzenlenmiştir. Yeni yapıda alıcı yerine bizim uygulamamızdaki veriler saklanmaktadır. 0 değeri reddedildi 1 değeri onaylandı anlamına gelmektedir.
Çalıştırmak için dosya dizini içerisinde :
python blockchain.py -p 5000 komutunu çalıştırmak yeterlidir.

2 uygulama aralarında http POST ile haberleşmektedir. Portlar hardcoded yazıldığı için yukarıda belirtilen portlarda çalıştırmak önemlidir!


