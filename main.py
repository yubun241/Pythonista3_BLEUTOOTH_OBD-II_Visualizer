from scene import *
import ui
import threading
import time
import random # デモ用

class GT500Monitor(Scene):
    def setup(self):
        self.background_color = '#050505'
        # データの初期化（通信スレッドと共有）
        self.data = {
            'rpm': 0, 'gear': 'N', 'water': 0, 'oil': 0, 
            'boost': 0.0, 'speed': 0
        }
        self.active = True
        
        # 通信専用スレッドを最高優先度で開始（実際のOBD通信用）
        self.comm_thread = threading.Thread(target=self.obd_comm_worker, daemon=True)
        self.comm_thread.start()

    def obd_comm_worker(self):
        """
        [通信専用スレッド] 
        UIの描画(120Hz)とは完全に独立して、iPhoneのCPUパワーを通信処理に全振りします。
        """
        while self.active:
            # TODO: ここに実際のBLE送信・受信処理を記述
            # 現在はデモ用に数値を高速シミュレーション
            self.data['rpm'] = (self.data['rpm'] + 100) % 8000
            if self.data['rpm'] > 7000:
                self.data['gear'] = random.choice(['1','2','3','4','5','6'])
            
            # 非常に短いスリープ、またはスリープなしで回すことで、
            # BLEのレスポンスが届き次第、即座に次のコマンドへ移る
            time.sleep(0.01) 

    def update(self):
        """
        [120Hz 描画アップデート]
        Sceneモジュールのこのメソッドは、ProMotionディスプレイの性能に合わせて
        最高速度で呼び出されます。
        """
        pass

    def draw(self):
        """
        [GPU描画] 
        """
        # --- 1. タコメーターバー (横) ---
        rpm_ratio = self.data['rpm'] / 8000
        bar_w = self.size.w - 100
        
        # 背景
        fill('#222')
        rect(50, self.size.h - 120, bar_w, 60)
        
        # メインバー（高回転で色変化）
        if rpm_ratio > 0.9: fill('#ff0000') # レブリミット
        elif rpm_ratio > 0.8: fill('#ffcc00') # シフトアップ警告
        else: fill('#00ff44') # 常用域
        
        rect(50, self.size.h - 120, bar_w * rpm_ratio, 60)

        # --- 2. センター・ギアポジション ---
        # 120Hzなので、ギアの切り替え時などのアニメーションも滑らかになります
        tint(1, 1, 1)
        text_draw_color = '#fff' if self.data['rpm'] < 7000 else '#ff0000'
        draw_text(self.data['gear'], font_size=250, 
                  x=self.size.w/2, y=self.size.h/2, color=text_draw_color)

        # --- 3. サイドの数値データ ---
        self.draw_metric("WATER", f"{92} C", 150, self.size.h/2 + 50)
        self.draw_metric("OIL", f"{105} C", 150, self.size.h/2 - 50)
        self.draw_metric("BOOST", f"{1.24:.2f}", self.size.w - 150, self.size.h/2)

    def draw_metric(self, label, value, x, y):
        draw_text(label, font_size=20, x=x, y=y+30, color='#aaa')
        draw_text(value, font_size=45, x=x, y=y, color='#fff')

def draw_text(txt, font_size, x, y, color='#fff'):
    render_text(txt, font_name='Helvetica-Bold', font_size=font_size)
    tint(color)
    text(txt, 'Helvetica-Bold', font_size, x, y)

if __name__ == '__main__':
    # 120Hzディスプレイをフル活用するための実行設定
    run(GT500Monitor(), orientation=LANDSCAPE, show_fps=True)
