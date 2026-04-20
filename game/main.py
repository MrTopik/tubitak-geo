import pygame
import sys
import random
import asyncio

pygame.init()
pygame.display.set_caption("Tasavvuf Ehli Bilgi Yarışması")

WIDTH, HEIGHT = 1200, 700
SIDEBAR_W = 320
MAP_W, MAP_H = WIDTH - SIDEBAR_W, HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BG_COLOR = (13, 17, 23)
PANEL_COLOR = (22, 27, 34)
GOLD = (201, 168, 76)
GOLD_DIM = (122, 92, 30)
TEAL = (42, 157, 143)
TEAL_LIGHT = (78, 205, 196)
CREAM = (240, 230, 211)
RED = (192, 57, 43)
GREEN = (39, 174, 96)
MUTED = (139, 115, 85)
WHITE = (255, 255, 255)

try:
    font_large = pygame.font.SysFont("georgia", 32, bold=True)
    font_medium = pygame.font.SysFont("georgia", 24)
    font_small = pygame.font.SysFont("georgia", 18)
    font_tiny = pygame.font.SysFont("georgia", 14)
except:
    font_large = pygame.font.Font(None, 40)
    font_medium = pygame.font.Font(None, 30)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)

try:
    map_image = pygame.image.load("Images/TrHarita.jpg")
    map_image = pygame.transform.smoothscale(map_image, (MAP_W, MAP_H))
except Exception as e:
    map_image = pygame.Surface((MAP_W, MAP_H))
    map_image.fill((30, 40, 40))

ROUTE_NAMES = [
    'İstanbul', 'Bursa', 'İzmir', 'Konya', 'Ankara',
    'Kayseri', 'Nevşehir', 'Sivas', 'Trabzon', 'Erzurum',
    'Van', 'Diyarbakır', 'Şanlıurfa', 'Gaziantep', 'Adana',
    'Hatay', 'Malatya', 'Elazığ', 'Erzincan', 'Samsun'
]

ROUTE_COORDS = [
    (130, 160),
    (160, 210),
    (80,  340),
    (330, 410),
    (350, 240),
    (480, 360),
    (430, 370),
    (560, 260),
    (670, 130),
    (780, 210),
    (850, 340),
    (710, 440),
    (630, 520),
    (570, 530),
    (470, 500),
    (510, 580),
    (600, 380),
    (650, 350),
    (690, 260),
    (530, 140) 
]

ALIMLER = [
    { 'name': 'Mevlânâ Celâleddin Rûmî', 'color': (232, 168, 56) },
    { 'name': 'Yunus Emre',               'color': (78, 205, 196) },
    { 'name': 'Hacı Bektaş-ı Velî',       'color': (167, 139, 250) },
    { 'name': 'Muhyiddin İbn Arabî',      'color': (251, 146, 60) },
    { 'name': 'İmam-ı Gazâlî',            'color': (52, 211, 153) },
    { 'name': 'Abdülkâdir-i Geylânî',     'color': (244, 114, 182) },
]

QUESTIONS = [
    { 'alim': 0, 'q': 'Mevlânâ\'nın "Mesnevi" adlı eseri kaç ciltten oluşmaktadır?', 'opts':['4','5','6','7'], 'ans':2 },
    { 'alim': 0, 'q': 'Mevlânâ Celâleddin Rûmî hangi şehirde doğmuştur?', 'opts':['Konya','Buhara','Belh','Semerkant'], 'ans':2 },
    { 'alim': 0, 'q': 'Mevlânâ\'nın semah dönerek yaptığı meditasyon ayinine ne ad verilir?', 'opts':['Sema','Zikir','Murakabe','Halvet'], 'ans':0 },
    { 'alim': 0, 'q': 'Mevlânâ\'nın en yakın dostu ve mürşidi kimdir?', 'opts':['Ateşbaz-ı Veli','Sultan Veled','Şems-i Tebrizî','Burhaneddin Muhakkik'], 'ans':2 },
    { 'alim': 0, 'q': 'Mevlânâ\'nın ölümüne verilen "Şeb-i Arûs" ne anlama gelir?', 'opts':['Hüzün Gecesi','Düğün Gecesi','Veda Gecesi','Kavuşma Gecesi'], 'ans':1 },
    { 'alim': 1, 'q': '"İlim ilim bilmektir, ilim kendin bilmektir..." dizesi kime aittir?', 'opts':['Mevlânâ','Hacı Bektaş','Yunus Emre','Pir Sultan'], 'ans':2 },
    { 'alim': 1, 'q': 'Yunus Emre hangi yüzyılda yaşamıştır?', 'opts':['12. yüzyıl','13-14. yüzyıl','15. yüzyıl','16. yüzyıl'], 'ans':1 },
    { 'alim': 1, 'q': 'Yunus Emre\'nin şiirlerini topladığı eserin adı nedir?', 'opts':['Divan','Mesnevi','Risalet','Makalat'], 'ans':0 },
    { 'alim': 1, 'q': 'Yunus Emre\'nin tasavvuf mürşidi kimdir?', 'opts':['Mevlânâ','Hacı Bektaş','Tapduk Emre','İbn Arabî'], 'ans':2 },
    { 'alim': 1, 'q': '"Biz gelmedik dâvâ için, bizim işimiz sevi için" diyen şair kimdir?', 'opts':['Pir Sultan Abdal','Yunus Emre','Niyazi Mısrî','Kaygusuz Abdal'], 'ans':1 },
    { 'alim': 2, 'q': 'Hacı Bektaş-ı Velî hangi ilde türbesi bulunur ve şehrin adıyla anılır?', 'opts':['Konya','Nevşehir','Kırşehir','Sivas'], 'ans':1 },
    { 'alim': 2, 'q': 'Hacı Bektaş-ı Velî\'nin kurucusu olduğu kabul edilen tarikat hangisidir?', 'opts':['Nakşibendilik','Mevlevilik','Bektaşilik','Kadirilik'], 'ans':2 },
    { 'alim': 2, 'q': 'Hacı Bektaş-ı Velî\'nin temel öğretisini özetleyen "Dört Kapı" nedir?', 'opts':['Şeriat-Tarikat-Marifet-Hakikat','İlim-Amel-Ahlak-İman','Zikir-Fikir-Şükür-Sabır','Namaz-Oruç-Hac-Zekat'], 'ans':0 },
    { 'alim': 2, 'q': 'Hacı Bektaş Velî\'nin Anadolu\'ya geldiği yer neresidir?', 'opts':['Irak','İran','Horasan','Yemen'], 'ans':2 },
    { 'alim': 3, 'q': 'Muhyiddin İbn Arabî\'nin "Fusûsu\'l-Hikem" eserinin Türkçe anlamı nedir?', 'opts':['Bilgeliklerin Özü','Kalplerin Dili','Aşkın Sırları','Hakikatin Aynası'], 'ans':0 },
    { 'alim': 3, 'q': 'İbn Arabî\'nin "Vahdet-i Vücûd" öğretisi ne anlama gelir?', 'opts':['İki Varlık','Varlığın Birliği','Çoklukta Birlik','Tanrının Görünmezliği'], 'ans':1 },
    { 'alim': 3, 'q': 'İbn Arabî hangi şehirde doğmuştur?', 'opts':['Bağdat','Kahire','Mürsiye','Şam'], 'ans':2 },
    { 'alim': 3, 'q': 'İbn Arabî\'ye verilen en yaygın lakap hangisidir?', 'opts':['Sultanü\'l-Evliya','Şeyhü\'l-Ekber','Kutbü\'l-Arifin','İmamü\'l-Müfessirin'], 'ans':1 },
    { 'alim': 4, 'q': 'İmam-ı Gazâlî\'nin en meşhur eseri "İhyâu Ulûmi\'d-Dîn"in anlamı nedir?', 'opts':['Din İlimlerinin Özü','Din İlimlerinin Yeniden Diriltilmesi','İslam\'ın Temelleri','Kalplerin İlacı'], 'ans':1 },
    { 'alim': 4, 'q': 'Gazâlî hangi şehirde doğmuştur?', 'opts':['Bağdat','Nişabur','Tus','İsfahan'], 'ans':2 },
    { 'alim': 4, 'q': 'Gazâlî\'nin filozoflara yönelik eleştiri kitabının adı nedir?', 'opts':['Tehâfütü\'l-Felâsife','Mişkâtü\'l-Envâr','Makâsıdü\'l-Felâsife','el-Munkız'], 'ans':0 },
    { 'alim': 4, 'q': 'Gazâlî hangi tarikatın kurucusunun müridi sayılır?', 'opts':['Kadirilik','Nakşibendilik','Rufailik','Yeseviyye'], 'ans':3 },
    { 'alim': 5, 'q': 'Abdülkâdir-i Geylânî\'nin kurduğu tarikat hangisidir?', 'opts':['Mevlevilik','Bektaşilik','Kadirilik','Halvetilik'], 'ans':2 },
    { 'alim': 5, 'q': 'Geylânî hangi ülkede doğmuştur (bugünkü coğrafya)?', 'opts':['Türkiye','Irak','İran','Suriye'], 'ans':2 },
    { 'alim': 5, 'q': 'Abdülkâdir-i Geylânî\'ye verilen "Gavs-ı Azam" lakabı ne anlama gelir?', 'opts':['En Büyük Kurtarıcı','Büyük Şeyh','Halkın Önderi','En Büyük Aşık'], 'ans':0 },
    { 'alim': 5, 'q': 'Geylânî\'nin en önemli eserlerinden biri olan "el-Fethu\'r-Rabbânî" ne tür bir eserdir?', 'opts':['Şiir divanı','Vaaz ve sohbet mecmuası','Tefsir kitabı','Fıkıh kitabı'], 'ans':1 },
]

class GameState:
    def __init__(self):
        self.pos = 0
        self.score = 0
        self.wrong = 0
        self.used_q = []
        self.current_q = None
        self.phase = 'board'
        self.result_correct = False
        self.particles = []

state = GameState()

def draw_text(surface, text, font, color, x, y, align="left", max_width=None):
    if max_width:
        words = text.split(" ")
        lines = []
        cur_line = []
        for word in words:
            cur_line.append(word)
            fw, fh = font.size(" ".join(cur_line))
            if fw > max_width:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))
        
        y_offset = y
        for line in lines:
            rendered = font.render(line, True, color)
            if align == "center":
                rect = rendered.get_rect(center=(x, y_offset))
                surface.blit(rendered, rect.topleft)
            else:
                surface.blit(rendered, (x, y_offset))
            y_offset += font.get_linesize()
        return y_offset
    else:
        rendered = font.render(text, True, color)
        rect = rendered.get_rect()
        if align == "center":
            rect.center = (x, y)
        elif align == "right":
            rect.topright = (x, y)
        else:
            rect.topleft = (x, y)
        surface.blit(rendered, rect.topleft)
        return y + font.get_linesize()

def draw_rounded_rect(surface, color, rect, radius=10, width=0):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)

def spawn_particles():
    colors = [GOLD, YELLOW := (232, 204, 122), TEAL_LIGHT, WHITE]
    for _ in range(30):
        px = random.randint(WIDTH//2 - 200, WIDTH//2 + 200)
        py = random.randint(HEIGHT//2 - 100, HEIGHT//2 + 100)
        vx = random.uniform(-4, 4)
        vy = random.uniform(-6, -2)
        c = random.choice(colors)
        state.particles.append([px, py, vx, vy, 1.0, c])

def update_particles():
    for p in state.particles:
        p[0] += p[2]
        p[1] += p[3]
        p[2] *= 0.98
        p[3] += 0.2
        p[4] -= 0.02
    state.particles = [p for p in state.particles if p[4] > 0]

def draw_particles():
    for p in state.particles:
        alpha = int(p[4] * 255)
        if alpha > 0:
            surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(surf, p[5] + (alpha,), (3, 3), 3)
            screen.blit(surf, (int(p[0]), int(p[1])))

def start_question():
    if state.phase != 'board':
        return
    
    available = [i for i in range(len(QUESTIONS)) if i not in state.used_q]
    if not available:
        available = list(range(len(QUESTIONS)))
        state.used_q = []
    
    q_idx = random.choice(available)
    state.used_q.append(q_idx)
    
    orig = QUESTIONS[q_idx]
    correct_text = orig['opts'][orig['ans']]
    
    shuffled_opts = orig['opts'].copy()
    random.shuffle(shuffled_opts)
    new_ans = shuffled_opts.index(correct_text)
    
    state.current_q = {
        'alim': orig['alim'],
        'q': orig['q'],
        'opts': shuffled_opts,
        'ans': new_ans
    }
    state.phase = 'question'

def answer_question(idx):
    if state.phase != 'question':
        return
    q = state.current_q
    is_correct = (idx == q['ans'])
    
    state.result_correct = is_correct
    if is_correct:
        state.score += 10
        state.pos = min(state.pos + 1, len(ROUTE_NAMES) - 1)
        spawn_particles()
    else:
        state.wrong += 1
        
    state.phase = 'result'

def close_result():
    if state.phase != 'result':
        return
    if state.pos == len(ROUTE_NAMES) - 1 and state.result_correct:
        state.phase = 'win'
    else:
        state.phase = 'board'

def restart_game():
    global state
    state = GameState()

def draw_board():
    screen.blit(map_image, (SIDEBAR_W, 0))
    
    overlay = pygame.Surface((MAP_W, MAP_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 70))
    screen.blit(overlay, (SIDEBAR_W, 0))

    for i, (cx, cy) in enumerate(ROUTE_COORDS):
        if i == state.pos:
            cx += SIDEBAR_W
            pygame.draw.circle(screen, (78, 205, 196, 100), (cx, cy), 18)
            pygame.draw.circle(screen, TEAL_LIGHT, (cx, cy), 10)
            pygame.draw.circle(screen, WHITE, (cx, cy), 5)
            draw_text(screen, f"📍 {ROUTE_NAMES[i]}", font_small, WHITE, cx, cy - 25, align="center")

    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, SIDEBAR_W, HEIGHT))
    pygame.draw.line(screen, GOLD_DIM, (SIDEBAR_W-1, 0), (SIDEBAR_W-1, HEIGHT), 2)
    
    draw_text(screen, "🕌 Tasavvuf Ehli Bilgi", font_medium, GOLD, SIDEBAR_W//2, 30, align="center")
    draw_text(screen, "Türkiye'nin Şehirleri", font_small, MUTED, SIDEBAR_W//2, 60, align="center")
    pygame.draw.line(screen, GOLD_DIM, (20, 90), (SIDEBAR_W-20, 90), 1)
    
    py = 110
    draw_text(screen, "✦ İlerleme ✦", font_small, GOLD, SIDEBAR_W//2, py, align="center")
    py += 35
    
    current_city = ROUTE_NAMES[state.pos]
    
    draw_text(screen, "Şehir:", font_small, MUTED, 30, py)
    draw_text(screen, current_city, font_medium, TEAL_LIGHT, SIDEBAR_W-30, py, align="right")
    py += 35
    draw_text(screen, "İlerleme:", font_small, MUTED, 30, py)
    draw_text(screen, f"{state.pos} / {len(ROUTE_NAMES)}", font_medium, CREAM, SIDEBAR_W-30, py, align="right")
    py += 35
    draw_text(screen, "Puan:", font_small, MUTED, 30, py)
    draw_text(screen, str(state.score), font_medium, GOLD, SIDEBAR_W-30, py, align="right")
    py += 35
    draw_text(screen, "Yanlış:", font_small, MUTED, 30, py)
    draw_text(screen, str(state.wrong), font_medium, RED, SIDEBAR_W-30, py, align="right")
    py += 40
    
    bar_rect = pygame.Rect(30, py, SIDEBAR_W - 60, 10)
    draw_rounded_rect(screen, (30, 40, 50), bar_rect, 5)
    fill_w = int((state.pos / len(ROUTE_NAMES)) * (SIDEBAR_W - 60))
    if fill_w > 0:
        fill_rect = pygame.Rect(30, py, fill_w, 10)
        draw_rounded_rect(screen, GOLD, fill_rect, 5)
    
    py += 50
    draw_text(screen, "📿 Büyük Alimler", font_small, GOLD, SIDEBAR_W//2, py, align="center")
    py += 30
    
    for i, alim in enumerate(ALIMLER):
        is_active = (state.phase == 'question' and state.current_q and state.current_q['alim'] == i)
        bg = (40, 50, 60) if is_active else (25, 30, 40)
        draw_rounded_rect(screen, bg, (20, py, SIDEBAR_W - 40, 30), 5)
        if is_active:
            draw_rounded_rect(screen, GOLD_DIM, (20, py, SIDEBAR_W - 40, 30), 5, 1)
        
        pygame.draw.circle(screen, alim['color'], (35, py + 15), 5)
        draw_text(screen, alim['name'], font_tiny, alim['color'], 45, py + 7)
        py += 35
    
    py = HEIGHT - 70
    draw_text(screen, "Soru Almak için BOŞLUK (SPACE) tuşuna bas", font_tiny, MUTED, SIDEBAR_W//2, py, align="center")

def draw_overlay_bg():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((5, 8, 20, 220))
    screen.blit(overlay, (0, 0))

def draw_question():
    draw_overlay_bg()
    q = state.current_q
    alim = ALIMLER[q['alim']]
    
    modal_w = 700
    modal_h = 400
    mx = (WIDTH - modal_w) // 2
    my = (HEIGHT - modal_h) // 2
    
    modal_rect = pygame.Rect(mx, my, modal_w, modal_h)
    draw_rounded_rect(screen, PANEL_COLOR, modal_rect, 20)
    draw_rounded_rect(screen, GOLD, modal_rect, 20, 2)
    
    draw_text(screen, "✦ " + alim['name'].upper() + " ✦", font_small, alim['color'], WIDTH//2, my + 30, align="center")
    
    draw_text(screen, q['q'], font_large, CREAM, WIDTH//2, my + 80, align="center", max_width=600)
    
    labels = ['1', '2', '3', '4']
    opt_w = 300
    opt_h = 50
    start_x = mx + 40
    start_y = my + 200
    
    for i, opt in enumerate(q['opts']):
        ox = start_x + (i % 2) * (opt_w + 20)
        oy = start_y + (i // 2) * (opt_h + 20)
        
        btn_rect = pygame.Rect(ox, oy, opt_w, opt_h)
        draw_rounded_rect(screen, (30, 40, 50), btn_rect, 10)
        draw_rounded_rect(screen, (80, 90, 100), btn_rect, 10, 1)
        
        pygame.draw.circle(screen, GOLD_DIM, (ox + 25, oy + 25), 15)
        draw_text(screen, labels[i], font_small, BG_COLOR, ox + 25, oy + 15, align="center")
        draw_text(screen, opt, font_tiny, WHITE, ox + 50, oy + 17)
        
        hx, hy = pygame.mouse.get_pos()
        if btn_rect.collidepoint(hx, hy):
            draw_rounded_rect(screen, GOLD_DIM, btn_rect, 10, 2)
            
    draw_text(screen, "Klavye: 1 · 2 · 3 · 4 veya Fare Rengi", font_tiny, MUTED, WIDTH//2, my + modal_h - 30, align="center")

def draw_result():
    draw_overlay_bg()
    
    modal_w = 500
    modal_h = 300
    mx = (WIDTH - modal_w) // 2
    my = (HEIGHT - modal_h) // 2
    
    modal_rect = pygame.Rect(mx, my, modal_w, modal_h)
    draw_rounded_rect(screen, PANEL_COLOR, modal_rect, 20)
    draw_rounded_rect(screen, GREEN if state.result_correct else RED, modal_rect, 20, 2)
    
    if state.result_correct:
        draw_text(screen, "✅", font_large, WHITE, WIDTH//2, my + 40, align="center")
        draw_text(screen, "Doğru!", font_large, GREEN, WIDTH//2, my + 100, align="center")
        draw_text(screen, "+10 Puan Kazandınız", font_medium, MUTED, WIDTH//2, my + 150, align="center")
        next_city = ROUTE_NAMES[state.pos]
        draw_text(screen, f"📍 Şimdi Mola: {next_city}", font_small, TEAL_LIGHT, WIDTH//2, my + 190, align="center")
    else:
        draw_text(screen, "❌", font_large, WHITE, WIDTH//2, my + 40, align="center")
        draw_text(screen, "Maalesef, yanlış!", font_large, RED, WIDTH//2, my + 100, align="center")
        corr = state.current_q['opts'][state.current_q['ans']]
        draw_text(screen, "Doğru Cevap:", font_small, MUTED, WIDTH//2, my + 150, align="center")
        draw_text(screen, corr, font_medium, CREAM, WIDTH//2, my + 180, align="center")
        
    draw_text(screen, "Devam etmek için BOŞLUK (SPACE)", font_tiny, MUTED, WIDTH//2, my + 260, align="center")

def draw_win():
    draw_overlay_bg()
    
    modal_w = 600
    modal_h = 400
    mx = (WIDTH - modal_w) // 2
    my = (HEIGHT - modal_h) // 2
    
    modal_rect = pygame.Rect(mx, my, modal_w, modal_h)
    draw_rounded_rect(screen, PANEL_COLOR, modal_rect, 20)
    draw_rounded_rect(screen, GOLD, modal_rect, 20, 2)
    
    draw_text(screen, "⭐ 🌙 ⭐", font_large, GOLD, WIDTH//2, my + 40, align="center")
    draw_text(screen, "Mânevî Yolculuk Tamamlandı!", font_large, GOLD, WIDTH//2, my + 100, align="center")
    
    hadisler = [
        "Nerede olursanız olun, Allah sizinle beraberdir. — Hadid 57/4",
        "Kalpler, ancak Allah'ın zikri ile huzur bulur. — Ra'd 13/28",
        "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin. — Hadis-i Şerif"
    ]
    idx = (state.score + state.wrong) % len(hadisler)
    
    draw_text(screen, hadisler[idx], font_tiny, TEAL_LIGHT, WIDTH//2, my + 160, align="center", max_width=500)
    
    draw_text(screen, f"Puan: {state.score}", font_medium, GOLD, mx + 150, my + 230, align="center")
    draw_text(screen, f"Yanlış: {state.wrong}", font_medium, RED, mx + 300, my + 230, align="center")
    grade = "🌟 Mükemmel" if state.wrong == 0 else "🥇 İyi" if state.wrong < 5 else "🥈 Orta" if state.wrong < 10 else "🥉 Başlangıç"
    draw_text(screen, grade, font_medium, CREAM, mx + 450, my + 230, align="center")
    
    draw_text(screen, "Yeniden Başlamak için 'R' Tuşuna Basın", font_small, MUTED, WIDTH//2, my + 330, align="center")

clock = pygame.time.Clock()
running = True

async def main():
    global state
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if state.phase == 'board':
                    if event.key == pygame.K_SPACE:
                        start_question()
                elif state.phase == 'question':
                    if event.key in (pygame.K_1, pygame.K_KP1): answer_question(0)
                    elif event.key in (pygame.K_2, pygame.K_KP2): answer_question(1)
                    elif event.key in (pygame.K_3, pygame.K_KP3): answer_question(2)
                    elif event.key in (pygame.K_4, pygame.K_KP4): answer_question(3)
                elif state.phase == 'result':
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        close_result()
                elif state.phase == 'win':
                    if event.key == pygame.K_r:
                        restart_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.phase == 'question':
                    hx, hy = event.pos
                    mx = (WIDTH - 700) // 2
                    my = (HEIGHT - 400) // 2
                    opt_w = 300
                    opt_h = 50
                    start_x = mx + 40
                    start_y = my + 200
                    for i in range(4):
                        ox = start_x + (i % 2) * (opt_w + 20)
                        oy = start_y + (i // 2) * (opt_h + 20)
                        if pygame.Rect(ox, oy, opt_w, opt_h).collidepoint(hx, hy):
                            answer_question(i)
                elif state.phase == 'result':
                    close_result()

        update_particles()

        screen.fill(BG_COLOR)
        
        draw_board()
        
        if state.phase == 'question':
            draw_question()
        elif state.phase == 'result':
            draw_result()
        elif state.phase == 'win':
            draw_win()
            
        draw_particles()

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
