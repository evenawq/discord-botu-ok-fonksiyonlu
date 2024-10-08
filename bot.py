import discord
from discord.ext import commands
import random
import requests
import sqlite3
import json
import os 
import eae

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f' AHALİ {bot.user} OLARAK GİRİŞ YAPTIK!')

@bot.command()
async def selam(ctx):
    await ctx.send(f"Selam {ctx.author}. Ben {bot.user}")

@bot.command()
async def rastgelesayi(ctx):
    # 1 ile 100 arasında rastgele bir sayı seç
    rastgele_sayi = random.randint(1, 100)
    # Sonucu gönder
    await ctx.send(f"Rastgele sayı: {rastgele_sayi}")

def tersten_yaz(yazi):
    return yazi[::-1]

girdi = "Merhaba Dünya"
ters_yazi = tersten_yaz(girdi)

print(f"Ters yazılmış hali: {ters_yazi}")

@bot.command()
async def aralik(ctx, s1: int = 2, s2: int = 3):
    a = 0
    for i in range(s1, s2 + 1):
        if i % 2 == 1:
            a += i
    await ctx.send(a)

@bot.command()
async def ciftler(ctx, s1: int = 2, s2: int = 3):
    toplam = 0
    for i in range(s1, s2 + 1):
        if i % 2 == 0:
            toplam += i
    await ctx.send(f"{s1} ile {s2} arasındaki çift sayıların toplamı: {toplam}")

@bot.command()
async def tekler(ctx, s1: int = 2, s2: int = 3):
    toplam = 0
    for i in range(s1, s2 + 1):
        if i % 2 == 1:
            toplam += i
    await ctx.send(f"{s1} ile {s2} arasındaki tek sayıların toplamı: {toplam}")

@bot.command()
async def terscevir(ctx, *, kelime: str):
    ters_kelime = kelime[::-1]
    await ctx.send(f"Orijinal kelime: {kelime}\nTers çevrilmiş hali: {ters_kelime}")

@bot.command()
async def saykelime(ctx, kelime: str, *, metin: str):
    kelime_sayisi = metin.lower().split().count(kelime.lower())
    await ctx.send(f"'{kelime}' kelimesi metin içinde {kelime_sayisi} kez geçiyor.")

jokes = [
    "Neden bilgisayar sıcak havalarda terler? Çünkü içinde 'fan' vardır.",
    "Matematik kitabı neden üzüldü? Çünkü çok problemi vardı.",
    "Işığı neden her zaman açarız? Çünkü karanlıkta gözlerimizle 'gör'üşemeyiz.",
    "Mantar neden dans eder? Çünkü o bir 'fungi' (fun guy)!",
    "Çatal ve bıçak kavga etti, kim kazandı? Hiçbiri, tabak araya girdi!"
    "Neden bilgisayar denize düştü? Çünkü fareyi düşürdü!",
    "Bir otobüs neden soğukta durur? Çünkü camları donmuş!",
    "Sakız neden okuldan atıldı? Çünkü sürekli yapışıyordu!",
    "Bir matematik kitabı neden üzgündü? Çünkü çok fazla problemi vardı!",
    "Bilgisayar neden terledi? Çünkü pencereyi açtı!",
    "Mikrofon neden konuşamadı? Çünkü kablosu koptu!",
    "Neden bilgisayar hiç uyuya kalmaz? Çünkü her zaman çalışıyor!",
    "Dondurma neden üzgün? Çünkü eriyor!"
]

# espri komutunu tanımlayın
@bot.command()
async def espri(ctx):
    espri = random.choice(jokes)
    await ctx.send(espri) 

API_KEY = 'ff4d0f71153fc14f03f0ef1410af08a9'

# hava komutunu tanımlayın
@bot.command()
async def hava(ctx, city: str):
    try:
        # API isteği yap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            await ctx.send(f"Hata: {data['message']}")
            return
        
        # Hava durumu bilgilerini al
        city_name = data["name"]
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Hava durumu bilgisini gönder
        weather_report = (
            f"{city_name} için hava durumu:\n"
            f"- Durum: {weather_description}\n"
            f"- Sıcaklık: {temperature}°C\n"
            f"- Hissedilen: {feels_like}°C\n"
            f"- Nem: %{humidity}\n"
            f"- Rüzgar Hızı: {wind_speed} m/s"
        )
        await ctx.send(weather_report)
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

conn = sqlite3.connect('jokes.db')
c = conn.cursor()

# Şaka tablosunu oluşturun
c.execute('''CREATE TABLE IF NOT EXISTS jokes (id INTEGER PRIMARY KEY AUTOINCREMENT, joke TEXT)''')
conn.commit()

# sakaekle komutunu tanımlayın
@bot.command()
async def sakaekle(ctx, *, joke: str):
    c.execute("INSERT INTO jokes (joke) VALUES (?)", (joke,))
    conn.commit()
    await ctx.send("Şaka eklendi!")

# saka komutunu tanımlayın
@bot.command()
async def saka(ctx):
    c.execute("SELECT joke FROM jokes")
    all_jokes = c.fetchall()
    if not all_jokes:
        await ctx.send("Veritabanında şaka bulunamadı.")
        return
    joke = random.choice(all_jokes)[0]
    await ctx.send(joke)

quotes = {
    "motivasyon": [
        "Başarı, sürekli çaba ve çalışma ile gelir.",
        "Yapabileceğinize inanıyorsanız, yaparsınız.",
        "En büyük zafer, asla düşmemekte değil, her düştüğünde tekrar ayağa kalkmaktadır."
    ],
    "bilim": [
        "Bilim, bilginin düzenlenmiş şeklidir.",
        "Bilim, cehaleti en aza indirme sanatıdır.",
        "Bir şeyi gerçekten anlamak için onu basitleştirin."
    ],
    "hayat": [
        "Hayat, sen planlar yaparken başına gelenlerdir.",
        "Hayat bir yolculuktur, varış noktası değil.",
        "Hayatın anlamı, anlam katmaktır."
    ]
}

# alinti komutunu tanımlayın
@bot.command()
async def alinti(ctx, konu: str):
    konu = konu.lower()
    if konu in quotes:
        alinti = random.choice(quotes[konu])
        await ctx.send(alinti)
    else:
        await ctx.send(f"{konu} hakkında alıntı bulunamadı. Mevcut konular: {', '.join(quotes.keys())}")

@bot.command()
async def rastgeleköpek(ctx):
    try:
        # API isteği yap
        response = requests.get("https://random.dog/woof.json")
        data = response.json()
        image_url = data["url"]
        
        # Resmi gönder
        await ctx.send(image_url)
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

colors = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Cyan": "#00FFFF",
    "Magenta": "#FF00FF",
    "Orange": "#FFA500",
    "Pink": "#FFC0CB",
    "Brown": "#A52A2A"
}

# rastgelerenk komutunu tanımlayın
@bot.command()
async def rastgelerenk(ctx):
    # Rastgele bir renk seç
    color_name, color_hex = random.choice(list(colors.items()))
    # Sonucu gönder
    await ctx.send(f"Rastgele renk: {color_name} - {color_hex}")

fun_facts = [
    "Dünyanın en uzun ağacı, Hyperion adlı bir Kızılçam'dır ve 115.7 metre uzunluğundadır.",
    "İnsan burnu 1 trilyondan fazla farklı kokuyu algılayabilir.",
    "Ahtapotların üç kalbi ve mavi kanı vardır.",
    "Bal arıları, dünyanın en zeki böceklerinden biridir ve birbirlerine yerleri dans ederek anlatırlar.",
    "Karıncalar uyumazlar, sadece ara sıra dinlenirler.",
    "Koalalar, parmak izleri insan parmak izlerine o kadar benzer ki, suç mahallerinde karışıklığa neden olabilirler.",
    "Jüpiter'in 79 tane uydusu vardır, bunların en büyüğü Ganymede'dir.",
    "Kutup ayıları kürkleri beyaz değil, şeffaftır; beyaz görünmelerinin nedeni ışığı yansıtmalarıdır."
]

# rastgelebilgi komutunu tanımlayın
@bot.command()
async def rastgelebilgi(ctx):
    # Rastgele bir bilgi seç
    bilgi = random.choice(fun_facts)
    # Sonucu gönder
    await ctx.send(f"İlginç bilgi: {bilgi}")

horoscope = {
    "Koç": "Bugün enerji dolu ve kararlısın. Hedeflerine ulaşmak için cesur adımlar atmalısın.",
    "Boğa": "Sabırlı olmayı hatırlamalısın. Bugün acele kararlar vermek yerine sakin kalmayı dene.",
    "İkizler": "Sosyal becerilerin bugün zirvede. Yeni insanlarla tanışmak için harika bir gün.",
    "Yengeç": "Duygusal olarak hassas bir gün olabilir. Kendine zaman ayır ve iç huzurunu bul.",
    "Aslan": "Liderlik özelliklerin bugün ön planda. Başkalarına yol gösterici olabilirsin.",
    "Başak": "Detaylara dikkat etmek seni başarıya götürecek. Bugün küçük şeylere odaklan.",
    "Terazi": "Dengeyi bulmak için mükemmel bir gün. Hem işte hem de özel hayatında uyum sağlamaya çalış.",
    "Akrep": "Tutkunun seni yönlendirmesine izin ver. Bugün tutkularının peşinden gitmelisin.",
    "Yay": "Macera seni çağırıyor. Yeni deneyimlere açık ol ve ufkunu genişlet.",
    "Oğlak": "Disiplin ve kararlılıkla hedeflerine ulaşabilirsin. Bugün azimle çalışmaya devam et.",
    "Kova": "Yaratıcı fikirlerinle öne çıkacaksın. Bugün yenilikçi düşüncelerinle fark yaratabilirsin.",
    "Balık": "Sezgilerin bugün güçlü. İç sesine kulak ver ve kalbinin sesini dinle."
}

# Burç hesaplama fonksiyonu
def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Koç"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Boğa"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "İkizler"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Yengeç"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Aslan"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Başak"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Terazi"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Akrep"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Yay"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Oğlak"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Kova"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Balık"

# burc_komut komutunu tanımlayın
@bot.command()
async def burc_komut(ctx, day: int, month: int):
    try:
        zodiac_sign = get_zodiac_sign(day, month)
        yorum = horoscope[zodiac_sign]
        await ctx.send(f"Burcun: {zodiac_sign}\nYorum: {yorum}")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

emojis = ['😀', '😂', '😍', '😎', '👍', '🔥', '✨', '🎉', '❤️', '💯']

# emoji_sifre komutunu tanımlayın
@bot.command()
async def emoji_sifre(ctx, length: int = 5):
    if length > 10:
        await ctx.send("Şifre uzunluğu en fazla 10 olabilir.")
    else:
        # Rastgele emojilerden oluşan bir şifre oluştur
        sifre = ''.join(random.choices(emojis, k=length))
        await ctx.send(f"İşte rastgele emoji şifreniz: {sifre}")

fun_facts = [
    "Dünyadaki okyanusların derinliği Everest Dağı'ndan daha fazladır.",
    "Bir bukalemun, dilini vücudundan 1.5 kat daha uzun fırlatabilir.",
    "Yarasalar, dünyada uçabilen tek memelilerdir.",
    "Dünyadaki en uzun süren gökkuşağı, 9 saat boyunca gökyüzünde kalmıştır.",
    "Bir insan hayatı boyunca yaklaşık 35 ton yiyecek tüketir.",
    "Plüton'un bir yılı, Dünya'nın 248 yılına eşittir.",
    "Yıldızlararası uzayda boşluk %99'dan daha fazla boşluktur.",
    "Balinaların şarkıları 1600 km öteden duyulabilir."
]

# gunluk_bilgi komutunu tanımlayın
@bot.command()
async def gunluk_bilgi(ctx):
    # Rastgele bir bilgi seç
    bilgi = random.choice(fun_facts)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün ilginç bilgisi: {bilgi}")

nature_facts = [
    "Bir yıldırımın sıcaklığı, Güneş'in yüzeyinden daha sıcak olabilir.",
    "Geyikler kışın beyaz renkte olan kürkleriyle karla örtülür, bu da onları kamufle eder.",
    "Dünyadaki en büyük volkan, Hawaii'deki Mauna Loa'dır.",
    "Bir kedi yaklaşık 32 farklı ses çıkarabilir.",
    "Arıların bal üretme süreci, her bir bal tabakası için 2 milyon çiçeği ziyaret etmeyi içerir.",
    "Dünyadaki en derin göl, Rusya'daki Baykal Gölü'dür ve derinliği yaklaşık 1642 metredir.",
    "Dünyanın en büyük çölü, Antarktika'dır, sıcaklık nedeniyle bu çöl 'soğuk çöl' olarak adlandırılır.",
    "Bir kara delik, tüm kütlesini tek bir noktada toplayarak uzay-zamanı bükebilir."
]

# doga_bilgi komutunu tanımlayın
@bot.command()
async def doga_bilgi(ctx):
    # Rastgele bir doğa bilgisi seç
    bilgi = random.choice(nature_facts)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün doğa bilgisi: {bilgi}")

documentary_recommendations = [
    "Planet Earth - Doğa belgeselinin en kapsamlı örneklerinden biri.",
    "The Blue Planet - Okyanusların derinliklerine dair inanılmaz görüntüler.",
    "Cosmos: A Spacetime Odyssey - Uzay ve evren hakkında kapsamlı bir keşif.",
    "The Social Dilemma - Sosyal medyanın topluma etkilerini inceleyen bir belgesel.",
    "13th - ABD'deki ceza adaleti sisteminin tarihi ve etkileri.",
    "Free Solo - Dağcı Alex Honnold'un El Capitan'ı serbest tırmanışını konu alır.",
    "Making a Murderer - Gerçek bir cinayet soruşturması ve yargılama sürecini araştırır.",
    "Our Planet - Doğal dünyamızın güzelliklerini ve tehditlerini keşfeder."
]

# belgesel_onerisi komutunu tanımlayın
@bot.command()
async def belgesel_onerisi(ctx):
    # Rastgele bir belgesel önerisi seç
    öneri = random.choice(documentary_recommendations)
    # Öneriyi gönder
    await ctx.send(f"Bugünün belgesel önerisi: {öneri}")

city_facts = [
    "Tokyo, Japonya'nın başkenti olup, dünyanın en kalabalık şehri olarak bilinir.",
    "New York City, Amerika Birleşik Devletleri'ndeki en kalabalık şehirlerden biridir ve 'Şehirler Şehri' olarak da adlandırılır.",
    "Paris, Fransa'nın başkenti olup, Eyfel Kulesi ve Louvre Müzesi gibi ünlü yapılarıyla tanınır.",
    "Istanbul, hem Asya hem de Avrupa kıtalarında bulunan tek şehir olup, tarihi boyunca birçok medeniyete ev sahipliği yapmıştır.",
    "Rio de Janeiro, Brezilya'nın ünlü plajları ve renkli karnavallarıyla bilinir.",
    "Cape Town, Güney Afrika'da bulunan ve muhteşem Table Mountain'a sahip bir şehirdir.",
    "Sydney, Avustralya'nın en büyük şehirlerinden biridir ve ünlü Sydney Opera Binası'na ev sahipliği yapar.",
    "Moskova, Rusya'nın başkenti olup, tarihi Kızıl Meydan ve Kremlin ile tanınır."
]

# sehir_bilgi komutunu tanımlayın
@bot.command()
async def sehir_bilgi(ctx):
    # Rastgele bir şehir bilgisi seç
    bilgi = random.choice(city_facts)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün şehir bilgisi: {bilgi}")

# Ücretsiz online araçlar listesi
online_tools = [
    "Canva: Grafik tasarımı yapabileceğiniz kullanımı kolay bir araçtır.",
    "Google Drive: Dosyalarınızı bulutta saklamanızı ve paylaşmanızı sağlar.",
    "Pixlr: Fotoğraf düzenleme için güçlü bir online araçtır.",
    "Trello: Projelerinizi yönetmek için işbirlikçi bir proje yönetim aracıdır.",
    "Grammarly: Yazılarınızın dilbilgisi ve yazım hatalarını kontrol eder.",
    "Slack: Ekipler arası iletişim ve işbirliği için kullanılan bir platformdur.",
    "JotForm: Çevrimiçi formlar oluşturmanıza yardımcı olur.",
    "Kahoot!: Eğitim amaçlı interaktif quizler oluşturabilir ve oynayabilirsiniz."
]

# online_arac komutunu tanımlayın
@bot.command()
async def online_arac(ctx):
    # Rastgele bir online araç bilgisi seç
    bilgi = random.choice(online_tools)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün online aracı: {bilgi}")

@bot.command()
async def kullanıcı_bilgisi(ctx, member: discord.Member = None):
    # Eğer üye belirtilmemişse, komutu gönderen kişiyi kullan
    if member is None:
        member = ctx.author

    # Üye bilgilerini al
    user_info = (
        f"**Kullanıcı Adı:** {member.name}\n"
        f"**Etiket:** {member.discriminator}\n"
        f"**ID:** {member.id}\n"
        f"**Hesap Oluşturulma Tarihi:** {member.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
        f"**Sunucuda Katılma Tarihi:** {member.joined_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
    )

    # Bilgiyi gönder
    await ctx.send(f"**Kullanıcı Bilgisi:**\n{user_info}")

@bot.command()
async def bilgikullanıcı(ctx, member: discord.Member = None):
    # Eğer üye belirtilmemişse, komutu gönderen kişiyi kullan
    if member is None:
        member = ctx.author

    # Üye bilgilerini al
    user_info = (
        f"**Kullanıcı Adı:** {member.name}\n"
        f"**Etiket:** {member.discriminator}\n"
        f"**ID:** {member.id}\n"
        f"**Hesap Oluşturulma Tarihi:** {member.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
        f"**Sunucuda Katılma Tarihi:** {member.joined_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
    )

    # Bilgiyi gönder
    await ctx.send(f"**Kullanıcı Bilgisi:**\n{user_info}")

@bot.command()
async def zarat(ctx):
    sonuc = random.randint(1, 6)
    await ctx.send(f"Zar sonucu: {sonuc}")

@bot.command()
async def yaz(ctx, *, metin):
    try:
        with open("discord_dosya.txt", "w") as dosya:
            dosya.write(metin)
        await ctx.send("Metin dosyaya yazıldı.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

@bot.command()
async def oku(ctx):
    try:
        with open("discord_dosya.txt", "r") as dosya:
            icerik = dosya.read()
        await ctx.send(f"Dosya içeriği: {icerik}")
    except FileNotFoundError:
        await ctx.send("Dosya bulunamadı.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

@bot.command()
async def dosyayaz(ctx, *, metin):
    try:
        with open("bot_dosya.txt", "w") as dosya:
            dosya.write(metin)
        await ctx.send("Metin dosyaya başarıyla yazıldı.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

@bot.command()
async def dosyaoku(ctx):
    try:
        if os.path.exists("bot_dosya.txt"):
            with open("bot_dosya.txt", "r") as dosya:
                icerik = dosya.read()
            await ctx.send(f"Dosya içeriği: {icerik}")
        else:
            await ctx.send("Dosya bulunamadı.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

@bot.command()
async def rastgele(ctx):
    """Sunucudaki rastgele bir kullanıcıyı seçer."""
    if len(ctx.guild.members) > 1:
        uye = random.choice(ctx.guild.members)
        await ctx.send(f"Rastgele seçilen kullanıcı: {uye.mention}")
    else:
        await ctx.send("Sunucuda yeterli üye bulunmuyor.")

data_file = 'points.json'

def load_points():
    """Puanları dosyadan yükler."""
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_points(points):
    """Puanları dosyaya kaydeder."""
    with open(data_file, 'w') as f:
        json.dump(points, f)

@bot.command()
async def puanver(ctx, miktar: int, uye: discord.Member):
    """Belirli bir üyeye puan verir."""
    points = load_points()
    
    if str(uye.id) not in points:
        points[str(uye.id)] = 0
    
    points[str(uye.id)] += miktar
    save_points(points)
    await ctx.send(f"{uye.mention} kullanıcısına {miktar} puan verildi!")

@bot.command()
async def puan(ctx, uye: discord.Member = None):
    """Kullanıcının puanını gösterir. Varsayılan olarak kendi puanınızı gösterir."""
    points = load_points()
    user_id = str(uye.id) if uye else str(ctx.author.id)
    
    if user_id in points:
        await ctx.send(f"{ctx.guild.get_member(int(user_id)).mention}'ın puanı: {points[user_id]}")
    else:
        await ctx.send("Bu kullanıcı için puan bulunamadı.")

oyuncular = [
    "Edin Dzeko: Mevkisi santrafordur Bosna Hersek doğumludur"
    "Dusan Tadic: Sol kanattır kendisi kaptanlık ruhuyla öne çıkar sırbistanlıdır"
    "Sebastian Szymanski: kendisi genelde ofansif bir oyuncudur ofansif ortasaha oynar skorerdir ve driblingleriyle oyuncuları geçmeyi sever"
    "Allan-Saint Maximin: Kendisi sol kanattır Dusan Tadic ile değişmeli olarak oynamaktadır. Maximin oynadığı zamanlarda Tadic Sağ kanat oynar. kendisinin lakabıda sihirbazdır"
    "FERDİ ERENAY KADIOĞLU: Kendisi Fenerbahçenin çocuğudur fenerbaçeye ilk geldiğinde daha sakalları yoktu ve ortasahaydı ancak şuanda Sola Bek oynuyor son zamanlarda Brightona yakın"
]

# online_arac komutunu tanımlayın
@bot.command()
async def Fenerbahçebilgi(ctx):
    # Rastgele bir online araç bilgisi seç
    bilgi = random.choice(oyuncular)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün online aracı: {bilgi}")

oyuncular = [
    "Dominik Livakovic - Kaleci, Hırvatistan",
    "İrfan Can Eğribayat - Kaleci, Türkiye",
    "Ertuğrul Çetin - Kaleci, Türkiye",
    "Furkan Akyüz - Kaleci, Türkiye",
    "Çağlar Söyüncü - Stoper, Türkiye",
    "Alexander Djiku - Stoper, Gana",
    "Rodrigo Becão - Stoper, Brezilya",
    "Samet Akaydin - Stoper, Türkiye",
    "Luan Peres - Stoper, Brezilya",
    "Omar Fayed - Stoper, Mısır",
    "Serdar Aziz - Stoper, Türkiye",
    "Yiğit Fidan - Stoper, Türkiye",
    "Ferdi Kadıoğlu - Sol Bek, Türkiye/Hollanda",
    "Jayden Oosterwolde - Sol Bek, Hollanda/Surinam",
    "Levent Mercan - Sol Bek, Türkiye/Almanya",
    "Bright Osayi-Samuel - Sağ Bek, Nijerya/İngiltere",
    "Mert Müldür - Sağ Bek, Türkiye/Avusturya",
    "İsmail Yüksek - Ön Libero, Türkiye",
    "Rade Krunic - Ön Libero, Bosna-Hersek",
    "Bartuğ Elmaz - Ön Libero, Türkiye",
    "Fred - Merkez Orta Saha, Brezilya",
    "Miguel Crespo - Merkez Orta Saha, Portekiz/Fransa",
    "Miha Zajc - Merkez Orta Saha, Slovenya",
    "Sebastian Szymanski - On Numara, Polonya",
    "Mert Hakan Yandaş - On Numara, Türkiye",
    "Allan Saint-Maximin - Sol Kanat, Fransa/Guadeloupe",
    "Dusan Tadic - Sol Kanat, Sırbistan",
    "Ryan Kent - Sol Kanat, İngiltere",
    "Cengiz Ünder - Sağ Kanat, Türkiye",
    "İrfan Can Kahveci - Sağ Kanat, Türkiye",
    "Oğuz Aydın - Sağ Kanat, Türkiye",
    "Emre Mor - Sağ Kanat, Türkiye/Danimarka",
    "Burak Kapacak - Sağ Kanat, Türkiye",
    "Youssef En-Nesyri - Santrafor, Fas",
    "João Pedro - Santrafor, İtalya/Brezilya",
    "Edin Dzeko - Santrafor, Bosna-Hersek",
    "Cenk Tosun - Santrafor, Türkiye"
]

# Bot komutunu tanımlayın (discord.py kullanarak)
@bot.command()
async def Fenerbahçe(ctx):
    # Rastgele bir futbolcu bilgisi seç
    bilgi = random.choice(oyuncular)
    # Bilgiyi gönder
    await ctx.send(f"Bugünün Fenerbahçeli futbolcusu: {bilgi}")

@bot.command()
async def fotoğraf_algılama(ctx):
    if ctx.message.attachments:
        for dosya in ctx.message.attachments:
            await dosya.save(f"./img/{dosya.filename}")
            await ctx.send("fotoğraf kaydedildi")
        sınıf,score=eae.efe(f"./img/{dosya.filename}")
        if sınıf=="geveze kuşu\n":
            await ctx.send("kuştur")
        elif sınıf==" Papasula abbotti\n":
            await ctx.send("Beslenme aralığı genellikle Christmas Adası'ndan 40-100 km'ye (25-62 mil) ulaşır")
        elif sınıf=="Habeş kara boynuzgagası\n":
            await ctx.send("üstgagalarından yukarı uzayan boynuzsu çıkıntı ile tanınır ve gagalar genelde rengarenk olur")
        elif sınıf=="taçlı turna\n":
            await ctx.send("Başın sert altın tüylerden oluşan bir tacı vardır. Yüzün yanları beyazdır ve parlak kırmızı, şişirilebilir bir boğaz kesesi vardır")
        elif sınıf=="Afrika zümrüt guguk kuşu\n":
            await ctx.send("kanatlıdır ve göç eder")
        elif sınıf=="Afrika ateş ispinozu\n":
            await ctx.send("kırmızıdır(!)")
        elif sınıf=="Haematopus moquini\n":
            await ctx.send("kuştur(!)")
        elif sınıf=="Lophoceros semifasciatus\n":
            await ctx.send("kuştur(!)")
        elif sınıf=="albatros\n":
            await ctx.send("beyazdır ve bir kuştur(!)")

bot.run("")
