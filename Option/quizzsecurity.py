import flet as ft

# -------------------- QUESTIONS (CYBERSECURITE) --------------------
questions = [
    {
        "question": "Qu’est-ce qu’une attaque brute force ?",
        "options": [
            "Une attaque physique",
            "Tester toutes les combinaisons possibles de mots de passe",
            "Un virus",
            "Un pare-feu"
        ],
        "answer": 1
    },
    {
        "question": "Que signifie HTTPS ?",
        "options": [
            "HyperText Transfer Protocol Secure",
            "High Transfer Text Protocol",
            "Secure Hyper Tool",
            "None"
        ],
        "answer": 0
    },
    {
        "question": "Quel est le rôle d’un firewall ?",
        "options": [
            "Accélérer internet",
            "Filtrer le trafic réseau",
            "Stocker les données",
            "Créer des mots de passe"
        ],
        "answer": 1
    },
    {
        "question": "Qu’est-ce qu’un malware ?",
        "options": [
            "Un logiciel sécurisé",
            "Un programme malveillant",
            "Un antivirus",
            "Un système d’exploitation"
        ],
        "answer": 1
    },
    {
        "question": "Qu’est-ce que le phishing ?",
        "options": [
            "Une technique de pêche",
            "Une attaque pour voler des données via faux sites/emails",
            "Un type de mot de passe",
            "Un protocole réseau"
        ],
        "answer": 1
    },
    {
        "question": "Que fait un VPN ?",
        "options": [
            "Accélère le PC",
            "Cache l’adresse IP et chiffre la connexion",
            "Supprime les virus",
            "Augmente le stockage"
        ],
        "answer": 1
    },
    {
        "question": "Qu’est-ce qu’une adresse IP ?",
        "options": [
            "Un mot de passe",
            "Un identifiant unique sur un réseau",
            "Un antivirus",
            "Un câble réseau"
        ],
        "answer": 1
    }
]

# -------------------- APP --------------------

def main(page: ft.Page):
    page.title = "Quiz Sécurité - Mots de Passe"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"

    score = 0
    current_q = 0

    question_text = ft.Text(size=28, weight="bold", color="white")
    feedback = ft.Text(size=18)
    options_column = ft.Column(spacing=15)
    progress = ft.ProgressBar(width=400, value=0)

    def update_question():
        options_column.controls.clear()
        feedback.value = ""

        q = questions[current_q]
        question_text.value = q["question"]
        progress.value = (current_q) / len(questions)

        for i, option in enumerate(q["options"]):
            btn = ft.Button(
                content=ft.Text(option, color="white"),
                width=400,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    bgcolor="#1e293b"
                ),
                on_click=lambda e, i=i: check_answer(i)
            )
            options_column.controls.append(btn)

        page.update()

    def check_answer(selected):
        nonlocal score, current_q

        correct = questions[current_q]["answer"]

        if selected == correct:
            score += 1
            feedback.value = "✅ Bonne réponse"
            feedback.color = "green"
        else:
            feedback.value = "❌ Mauvaise réponse"
            feedback.color = "red"

        current_q += 1

        if current_q < len(questions):
            page.update()
            page.run_task(delayed_next)
        else:
            show_result()

    async def delayed_next():
        import asyncio
        await asyncio.sleep(1)
        update_question()

    def show_result():
        page.controls.clear()

        result = ft.Column(
            [
                ft.Text("Quiz terminé 🎉", size=40, weight="bold"),
                ft.Text(f"Score: {score}/{len(questions)}", size=30),
                ft.Button("Recommencer", on_click=restart)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(result)

    def restart(e):
        nonlocal score, current_q
        score = 0
        current_q = 0
        page.controls.clear()
        build_ui()

    def build_ui():
        container = ft.Container(
            content=ft.Column(
                [
                    question_text,
                    options_column,
                    feedback,
                    progress
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25
            ),
            padding=30,
            border_radius=20,
            bgcolor="#020617",
            width=500
        )

        page.add(
            ft.Row(
                [container],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

        update_question()

    build_ui()