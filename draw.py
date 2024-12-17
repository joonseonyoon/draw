import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# 1~500 숫자 리스트 생성
numbers = list(range(1, 501))

# 등수별 당첨자 저장
winners = {
    "1등": [],
    "2등": [],
    "3등": [],
    "4등": []
}

# 취소된 번호 저장
cancelled_numbers = []

# 특정 번호 유효성 확인 함수
def is_valid_winner(number):
    return number % 2 == 0

# 랜덤 번호 애니메이션 함수
def animate_random_numbers(label, duration, callback):
    def update_label():
        if duration[0] > 0:
            random_number = random.choice(numbers)
            label.config(text=f"추첨 중...\n{random_number}")
            duration[0] -= 0.1
            label.after(100, update_label)
        else:
            callback()

    update_label()

# 당첨 함수
def draw_winners(rank, count):
    global numbers
    if len(numbers) < count:
        messagebox.showerror("오류", "추첨 가능한 숫자가 부족합니다!")
        return

    if winners[rank]:
        messagebox.showwarning("알림", f"{rank} 추첨은 이미 완료되었습니다!")
        return

    selected = []
    while len(selected) < count:
        candidate = random.choice(numbers)
        if is_valid_winner(candidate):
            selected.append(candidate)
            numbers.remove(candidate)

    def reveal_next(index):
        if index < len(selected):
            # 번호 애니메이션 시작
            animate_random_numbers(result_label, [2], lambda: show_winner(index))
        else:
            messagebox.showinfo("추첨 완료", f"{rank} 추첨이 완료되었습니다!")

    def show_winner(index):
        # 최종 번호 표시
        result_label.config(text=f"당첨 번호: {selected[index]}")
        winners[rank].append(selected[index])
        update_side_label()
        # 1초 후 다음 번호 추첨
        result_label.after(1000, reveal_next, index + 1)

    reveal_next(0)

# 오른쪽 라벨 업데이트
def update_side_label():
    side_text = ""
    for rank, nums in winners.items():
        if nums:
            side_text += f"{rank}:\n"
            for num in nums:
                if num in cancelled_numbers:
                    side_text += f"❌ {num}\n"  # 취소된 번호에 표시
                else:
                    side_text += f"{num}\n"
            side_text += "\n"
    side_label.config(text=side_text, font=("Arial", 18, "bold"), justify="center")
    side_canvas.update_idletasks()
    side_canvas.config(scrollregion=side_canvas.bbox("all"))

# 취소된 번호를 빨간색으로 표시
def cancel_number():
    try:
        cancel_num = int(cancel_entry.get())
        if cancel_num not in sum(winners.values(), []):
            messagebox.showinfo("알림", "입력한 번호가 당첨 번호에 없습니다.")
        elif cancel_num in cancelled_numbers:
            messagebox.showinfo("알림", "이미 취소된 번호입니다.")
        else:
            cancelled_numbers.append(cancel_num)
            update_side_label()
    except ValueError:
        messagebox.showerror("오류", "숫자를 입력하세요.")

# 한 명 더 추첨
def draw_one_more():
    rank = rank_entry.get()
    if rank not in winners:
        messagebox.showerror("오류", "올바른 등수를 입력하세요.")
        return
    if len(numbers) < 1:
        messagebox.showerror("오류", "추첨 가능한 숫자가 부족합니다!")
        return

    def show_final_winner():
        selected = random.choice(numbers)
        numbers.remove(selected)
        winners[rank].append(selected)
        update_side_label()
        messagebox.showinfo("추가 추첨 완료", f"{rank}에 번호 {selected}가 추가되었습니다!")

    # 번호 애니메이션 시작
    animate_random_numbers(result_label, [3], show_final_winner)

# GUI 설정
app = tk.Tk()
app.title("2024 크리스마스 이브 경품 추첨!!! ^^")
app.geometry("1000x600")

# 배경 이미지 설정
bg_image = Image.open("snowy_field.jpg")
bg_image = bg_image.resize((1000, 600))#, Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(app, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# 메인 프레임
main_frame = tk.Frame(app, bg="white")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# 왼쪽 버튼 프레임
button_frame = tk.Frame(main_frame, bg="white")
button_frame.pack(side="left", fill="y", padx=10)

# 결과 표시 라벨 (중앙)
result_label = tk.Label(main_frame, text="결과가 여기에 표시됩니다.", font=("Arial", 24), bg="white", justify="center")
result_label.pack(side="left", fill="both", expand=True, padx=20)

# 오른쪽 스크롤 가능한 캔버스
side_canvas = tk.Canvas(main_frame, bg="white")
side_canvas.pack(side="right", fill="both", expand=True)

# 스크롤바 추가
side_scrollbar = tk.Scrollbar(app, orient="vertical", command=side_canvas.yview)
side_scrollbar.pack(side="right", fill="y")

side_canvas.configure(yscrollcommand=side_scrollbar.set)

# 오른쪽 내부 프레임
side_frame = tk.Frame(side_canvas, bg="white")
side_canvas.create_window((0, 0), window=side_frame, anchor="nw")

# 라벨 추가
side_label = tk.Label(side_frame, text="", font=("Arial", 18, "bold"), bg="white", fg="blue", justify="center", anchor="n")
side_label.pack(fill="both", expand=True)

# 입력 영역
input_frame = tk.Frame(app, bg="white")
input_frame.pack(fill="x", padx=20, pady=10)

tk.Label(input_frame, text="취소할 번호 입력:", bg="white", font=("Arial", 12)).pack(side="left", padx=5)
cancel_entry = tk.Entry(input_frame, font=("Arial", 12))
cancel_entry.pack(side="left", padx=5)
cancel_button = tk.Button(input_frame, text="취소선 추가", command=cancel_number, font=("Arial", 12))
cancel_button.pack(side="left", padx=5)

tk.Label(input_frame, text="등수 입력:", bg="white", font=("Arial", 12)).pack(side="left", padx=5)
rank_entry = tk.Entry(input_frame, font=("Arial", 12))
rank_entry.pack(side="left", padx=5)
extra_button = tk.Button(input_frame, text="한 명 더 추첨", command=draw_one_more, font=("Arial", 12))
extra_button.pack(side="left", padx=5)

# 추첨 버튼
btn_1st = tk.Button(button_frame, text="1등 추첨 (1명)", font=("Arial", 14), command=lambda: draw_winners("1등", 1))
btn_1st.pack(anchor="w", pady=10)

btn_2nd = tk.Button(button_frame, text="2등 추첨 (3명)", font=("Arial", 14), command=lambda: draw_winners("2등", 3))
btn_2nd.pack(anchor="w", pady=10)

btn_3rd = tk.Button(button_frame, text="3등 추첨 (5명)", font=("Arial", 14), command=lambda: draw_winners("3등", 5))
btn_3rd.pack(anchor="w", pady=10)

btn_4th = tk.Button(button_frame, text="4등 추첨 (10명)", font=("Arial", 14), command=lambda: draw_winners("4등", 10))
btn_4th.pack(anchor="w", pady=10)

# 앱 실행
app.mainloop()
