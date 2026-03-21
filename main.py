# ============================================================
#   تطبيق القرآن الكريم - بصوت الشيخ ناصر القطامي
# ============================================================

import os
import threading
import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex("#0D1F1A")

# ── Register Arabic font ─────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Amiri-Regular.ttf")

if os.path.exists(FONT_PATH):
    LabelBase.register(name="Arabic", fn_regular=FONT_PATH)
    ARABIC_FONT = "Arabic"
else:
    ARABIC_FONT = "Roboto"   # fallback

# ── Audio source ─────────────────────────────────────────────
BASE_URL  = "https://server8.mp3quran.net/qtm/"
AUDIO_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(AUDIO_DIR, exist_ok=True)

# ── Colors ───────────────────────────────────────────────────
BG_DARK     = get_color_from_hex("#0D1F1A")
BG_CARD     = get_color_from_hex("#152B23")
GREEN_MAIN  = get_color_from_hex("#2ECC71")
GREEN_LIGHT = get_color_from_hex("#A8E6C3")
GOLD        = get_color_from_hex("#D4AF37")
WHITE       = get_color_from_hex("#F5F5F5")
GRAY        = get_color_from_hex("#8A9A8E")
RED         = get_color_from_hex("#E74C3C")

# ── All 114 Surahs ───────────────────────────────────────────
SURAHS = [
    (1,"الفاتحة",7),(2,"البقرة",286),(3,"آل عمران",200),(4,"النساء",176),
    (5,"المائدة",120),(6,"الأنعام",165),(7,"الأعراف",206),(8,"الأنفال",75),
    (9,"التوبة",129),(10,"يونس",109),(11,"هود",123),(12,"يوسف",111),
    (13,"الرعد",43),(14,"إبراهيم",52),(15,"الحجر",99),(16,"النحل",128),
    (17,"الإسراء",111),(18,"الكهف",110),(19,"مريم",98),(20,"طه",135),
    (21,"الأنبياء",112),(22,"الحج",78),(23,"المؤمنون",118),(24,"النور",64),
    (25,"الفرقان",77),(26,"الشعراء",227),(27,"النمل",93),(28,"القصص",88),
    (29,"العنكبوت",69),(30,"الروم",60),(31,"لقمان",34),(32,"السجدة",30),
    (33,"الأحزاب",73),(34,"سبأ",54),(35,"فاطر",45),(36,"يس",83),
    (37,"الصافات",182),(38,"ص",88),(39,"الزمر",75),(40,"غافر",85),
    (41,"فصلت",54),(42,"الشورى",53),(43,"الزخرف",89),(44,"الدخان",59),
    (45,"الجاثية",37),(46,"الأحقاف",35),(47,"محمد",38),(48,"الفتح",29),
    (49,"الحجرات",18),(50,"ق",45),(51,"الذاريات",60),(52,"الطور",49),
    (53,"النجم",62),(54,"القمر",55),(55,"الرحمن",78),(56,"الواقعة",96),
    (57,"الحديد",29),(58,"المجادلة",22),(59,"الحشر",24),(60,"الممتحنة",13),
    (61,"الصف",14),(62,"الجمعة",11),(63,"المنافقون",11),(64,"التغابن",18),
    (65,"الطلاق",12),(66,"التحريم",12),(67,"الملك",30),(68,"القلم",52),
    (69,"الحاقة",52),(70,"المعارج",44),(71,"نوح",28),(72,"الجن",28),
    (73,"المزمل",20),(74,"المدثر",56),(75,"القيامة",40),(76,"الإنسان",31),
    (77,"المرسلات",50),(78,"النبأ",40),(79,"النازعات",46),(80,"عبس",42),
    (81,"التكوير",29),(82,"الانفطار",19),(83,"المطففين",36),(84,"الانشقاق",25),
    (85,"البروج",22),(86,"الطارق",17),(87,"الأعلى",19),(88,"الغاشية",26),
    (89,"الفجر",30),(90,"البلد",20),(91,"الشمس",15),(92,"الليل",21),
    (93,"الضحى",11),(94,"الشرح",8),(95,"التين",8),(96,"العلق",19),
    (97,"القدر",5),(98,"البينة",8),(99,"الزلزلة",8),(100,"العاديات",11),
    (101,"القارعة",11),(102,"التكاثر",8),(103,"العصر",3),(104,"الهمزة",9),
    (105,"الفيل",5),(106,"قريش",4),(107,"الماعون",7),(108,"الكوثر",3),
    (109,"الكافرون",6),(110,"النصر",3),(111,"المسد",5),(112,"الإخلاص",4),
    (113,"الفلق",5),(114,"الناس",6),
]

def local_path(n):
    return os.path.join(AUDIO_DIR, f"{n:03d}.mp3")

def is_downloaded(n):
    p = local_path(n)
    return os.path.exists(p) and os.path.getsize(p) > 1000

def AR(text, size, bold=False, color=WHITE, halign="right"):
    """Helper: create a Label with the Arabic font"""
    return Label(
        text=text,
        font_name=ARABIC_FONT,
        font_size=size,
        bold=bold,
        color=color,
        halign=halign,
        text_size=(None, None),
    )


# ════════════════════════════════════════════════════════════
#  SURAH ROW
# ════════════════════════════════════════════════════════════
class SurahRow(BoxLayout):
    def __init__(self, surah, on_play, **kw):
        super().__init__(orientation="horizontal",
                         size_hint_y=None, height=dp(68),
                         spacing=dp(6), padding=[dp(10), dp(6)], **kw)
        self.surah   = surah
        self.on_play = on_play
        self._busy   = False

        with self.canvas.before:
            Color(*BG_CARD)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._upd, size=self._upd)

        num, arabic, verses = surah

        # Number badge
        self.add_widget(Label(
            text=str(num), size_hint_x=None, width=dp(34),
            font_size=dp(13), color=GOLD, bold=True))

        # Name + verses
        col = BoxLayout(orientation="vertical")
        col.add_widget(AR(arabic, dp(17), bold=True, color=WHITE, halign="right"))
        col.add_widget(AR(f"{verses} آية", dp(11), color=GRAY, halign="right"))
        self.add_widget(col)

        # Action button
        self.btn = Button(
            size_hint_x=None, width=dp(76), height=dp(46),
            font_name=ARABIC_FONT, font_size=dp(12),
            background_normal="", on_press=self._act)
        self.add_widget(self.btn)

        # Delete button
        self.btn_del = Button(
            text="🗑", size_hint_x=None, width=dp(40), height=dp(46),
            font_size=dp(18), background_normal="",
            background_color=(*RED[:3], 0.15),
            color=RED, on_press=self._delete)
        self.add_widget(self.btn_del)

        self._refresh()

    def _upd(self, *a):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _refresh(self):
        if is_downloaded(self.surah[0]):
            self.btn.text             = "▶ تشغيل"
            self.btn.background_color = (*GREEN_MAIN[:3], 1)
            self.btn.color            = BG_DARK
            self.btn_del.opacity      = 1
            self.btn_del.disabled     = False
        else:
            self.btn.text             = "↓ تحميل"
            self.btn.background_color = (*GOLD[:3], 0.9)
            self.btn.color            = BG_DARK
            self.btn_del.opacity      = 0
            self.btn_del.disabled     = True

    def _act(self, *a):
        if is_downloaded(self.surah[0]):
            self.on_play(self.surah)
        elif not self._busy:
            self._download()

    def _download(self):
        self._busy = True
        self.btn.text             = "0%"
        self.btn.background_color = (*GRAY[:3], 0.5)
        self.btn.disabled         = True

        num  = self.surah[0]
        url  = BASE_URL + f"{num:03d}.mp3"
        dest = local_path(num)

        def run():
            try:
                r = requests.get(url, stream=True, timeout=30)
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                done  = 0
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                            done += len(chunk)
                            if total:
                                self._pct(int(done / total * 100))
                self._done(True)
            except Exception:
                self._done(False)

        threading.Thread(target=run, daemon=True).start()

    @mainthread
    def _pct(self, p): self.btn.text = f"{p}%"

    @mainthread
    def _done(self, ok):
        self._busy = False
        self.btn.disabled = False
        if ok:
            self._refresh()
        else:
            self.btn.text             = "✗ أعد المحاولة"
            self.btn.background_color = (*RED[:3], 0.8)
            self.btn.color            = WHITE
            Clock.schedule_once(lambda dt: self._refresh(), 3)

    def _delete(self, *a):
        p = local_path(self.surah[0])
        if os.path.exists(p): os.remove(p)
        self._refresh()


# ════════════════════════════════════════════════════════════
#  SURAH LIST SCREEN
# ════════════════════════════════════════════════════════════
class SurahListScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical")

        # Header
        hdr = BoxLayout(size_hint_y=None, height=dp(88), padding=[dp(14), dp(8)])
        with hdr.canvas.before:
            Color(*BG_CARD)
            self._hr = Rectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda w,_: setattr(self._hr,'pos',w.pos),
                 size=lambda w,_: setattr(self._hr,'size',w.size))
        col = BoxLayout(orientation="vertical")
        col.add_widget(AR("القرآن الكريم", dp(26), bold=True, color=GOLD, halign="center"))
        col.add_widget(AR("الشيخ ناصر القطامي", dp(13), color=GREEN_LIGHT, halign="center"))
        hdr.add_widget(col)
        root.add_widget(hdr)

        root.add_widget(AR("اضغط ↓ تحميل  ·  ▶ تشغيل  ·  🗑 حذف",
                           dp(11), color=GRAY, halign="center"))

        sv = ScrollView()
        self.box = BoxLayout(orientation="vertical", size_hint_y=None,
                             spacing=dp(4), padding=[dp(8), dp(4)])
        self.box.bind(minimum_height=self.box.setter("height"))
        for s in SURAHS:
            self.box.add_widget(SurahRow(s, on_play=self._play))
        sv.add_widget(self.box)
        root.add_widget(sv)
        self.add_widget(root)

    def _play(self, surah):
        p = self.manager.get_screen("player")
        p.load_surah(surah)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "player"

    def on_enter(self):
        for row in self.box.children:
            if isinstance(row, SurahRow):
                row._refresh()


# ════════════════════════════════════════════════════════════
#  PLAYER SCREEN
# ════════════════════════════════════════════════════════════
class PlayerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sound   = None
        self.playing = False
        self._clk    = None
        self._surah  = SURAHS[0]
        self._build_ui()

    def _build_ui(self):
        r = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(18))

        back = Button(text="← القائمة", size_hint_y=None, height=dp(44),
                      font_name=ARABIC_FONT, background_normal="",
                      background_color=BG_CARD, color=GREEN_LIGHT,
                      font_size=dp(14), on_press=self.back)
        r.add_widget(back)

        self.lbl_name = AR("", dp(32), bold=True, color=GOLD, halign="center")
        r.add_widget(self.lbl_name)

        r.add_widget(AR("الشيخ ناصر القطامي", dp(13), color=GREEN_LIGHT, halign="center"))

        self.lbl_v = AR("", dp(12), color=GRAY, halign="center")
        r.add_widget(self.lbl_v)

        r.add_widget(Label(size_hint_y=0.1))
        r.add_widget(AR("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                        dp(18), color=WHITE, halign="center"))
        r.add_widget(Label(size_hint_y=0.25))

        self.prog = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(6))
        r.add_widget(self.prog)

        tr = BoxLayout(size_hint_y=None, height=dp(24))
        self.lbl_e = Label(text="0:00", font_size=dp(12), color=GRAY)
        self.lbl_t = Label(text="0:00", font_size=dp(12), color=GRAY, halign="right")
        tr.add_widget(self.lbl_e); tr.add_widget(self.lbl_t)
        r.add_widget(tr)

        r.add_widget(Label(size_hint_y=0.05))

        ctrl = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(14))
        ctrl.add_widget(Button(text="⏮", font_size=dp(28), background_normal="",
                               background_color=BG_CARD, color=GREEN_LIGHT,
                               on_press=self.prev))
        self.btn_play = Button(text="▶", font_size=dp(34), bold=True,
                               background_normal="", background_color=GREEN_MAIN,
                               color=BG_DARK, on_press=self.toggle)
        ctrl.add_widget(self.btn_play)
        ctrl.add_widget(Button(text="⏭", font_size=dp(28), background_normal="",
                               background_color=BG_CARD, color=GREEN_LIGHT,
                               on_press=self.next))
        r.add_widget(ctrl)

        self.lbl_st = AR("", dp(12), color=GRAY, halign="center")
        r.add_widget(self.lbl_st)
        r.add_widget(Label(size_hint_y=0.1))
        self.add_widget(r)

    def load_surah(self, surah):
        self._stop()
        self._surah = surah
        num, arabic, verses = surah
        self.lbl_name.text = arabic
        self.lbl_v.text    = f"عدد الآيات: {verses}"
        self.prog.value    = 0
        self.lbl_e.text    = "0:00"
        self.lbl_t.text    = "0:00"
        self.btn_play.text = "▶"

        if is_downloaded(num):
            self.sound = SoundLoader.load(local_path(num))
            self.lbl_st.text = "جاهز ✓" if self.sound else "⚠ فشل"
        else:
            self.lbl_st.text = "⚠ السورة غير محملة"

    def toggle(self, *a):
        if not self.sound:
            self.lbl_st.text = "⚠ لا يوجد ملف صوتي"
            return
        if self.playing:
            self.sound.stop(); self.playing = False
            self.btn_play.text = "▶"; self.lbl_st.text = "متوقف"
            if self._clk: self._clk.cancel()
        else:
            self.sound.play(); self.playing = True
            self.btn_play.text = "⏸"; self.lbl_st.text = "جاري التشغيل ..."
            self._clk = Clock.schedule_interval(self._tick, 0.5)

    def _tick(self, dt):
        if not (self.sound and self.playing): return
        pos = self.sound.get_pos(); dur = self.sound.length or 0
        if dur > 0:
            self.prog.value = pos / dur * 100
            self.lbl_e.text = self._f(pos); self.lbl_t.text = self._f(dur)
            if pos >= dur - 0.5: self.next()

    def next(self, *a):
        idx = self._surah[0]
        if idx < 114:
            self.load_surah(SURAHS[idx])
            if is_downloaded(SURAHS[idx][0]): self.toggle()

    def prev(self, *a):
        idx = self._surah[0]
        if idx > 1:
            self.load_surah(SURAHS[idx - 2])
            if is_downloaded(SURAHS[idx - 2][0]): self.toggle()

    def back(self, *a):
        self._stop()
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "list"

    def _stop(self):
        if self.sound: self.sound.stop(); self.sound.unload(); self.sound = None
        self.playing = False
        if self._clk: self._clk.cancel()

    @staticmethod
    def _f(s): return f"{int(s)//60}:{int(s)%60:02d}"


# ════════════════════════════════════════════════════════════
#  APP
# ════════════════════════════════════════════════════════════
class QuranApp(App):
    title = "القرآن الكريم"
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SurahListScreen(name="list"))
        sm.add_widget(PlayerScreen(name="player"))
        return sm

if __name__ == "__main__":
    QuranApp().run()
