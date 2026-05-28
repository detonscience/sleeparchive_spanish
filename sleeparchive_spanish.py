import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Rescate 4AM", page_icon="🌙", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #050510 0%, #0d0d1c 55%, #15152a 100%);
    color: #f2f0ff;
}
h1, h2, h3, p, label, span, div {
    color: #f2f0ff !important;
}
section[data-testid="stSidebar"] {
    background-color: #080814;
}
div.stButton > button {
    width: 100%;
    background-color: #24244a;
    color: #ffffff;
    border-radius: 18px;
    border: 1px solid #6b6bb0;
    padding: 0.8rem 1rem;
    font-size: 17px;
}
div.stButton > button:hover {
    border: 1px solid #aaaaff;
    background-color: #303060;
}
div[data-testid="stLinkButton"] a {
    width: 100% !important;
    color: #ffffff !important;
    background-color: #24244a !important;
    border: 1px solid #6b6bb0 !important;
    border-radius: 18px !important;
    font-weight: 700 !important;
    padding: 0.8rem 1rem !important;
    text-decoration: none !important;
}
div[data-testid="stLinkButton"] a:hover {
    color: #ffffff !important;
    border: 1px solid #aaaaff !important;
    background-color: #303060 !important;
}
div[data-testid="stLinkButton"] a p {
    color: #ffffff !important;
    font-weight: 700 !important;
}
textarea, input {
    background-color: #101020 !important;
    color: #f2f0ff !important;
}
.small-note {
    opacity: 0.8;
    font-size: 0.95rem;
}
.calm-card {
    padding: 1rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

if "wake_log" not in st.session_state:
    st.session_state.wake_log = []
if "parked_thoughts" not in st.session_state:
    st.session_state.parked_thoughts = []
if "activity_done" not in st.session_state:
    st.session_state.activity_done = []

messages = [
    "Estás a salvo. No tienes que resolver nada en este momento.",
    "No negocies con los pensamientos de las 4 AM.",
    "Descansar también cuenta, aunque el sueño tarde en regresar.",
    "Tu yo de mañana puede manejar esto. Tu yo de las 4 AM solo necesita descansar.",
    "Esto es un despertar, no una crisis. Deja que el cuerpo se vuelva pesado otra vez."
]

activities = {
    "Mi mente está acelerada": {
        "title": "🧺 Canasta de pensamientos",
        "intro": "Tu cerebro está intentando mantenerte alerta. Vamos a darle un lugar para dejar las cosas por ahora.",
        "steps": [
            "Escribe el pensamiento principal en una sola oración.",
            "Dite a ti mismo: ya guardé esto para mañana.",
            "Pon una mano sobre tu pecho y exhala lentamente.",
            "Imagina que ese pensamiento está en una canasta cerrada fuera del cuarto."
        ]
    },
    "Me siento ansioso": {
        "title": "🫁 Respiración 4-2-6",
        "intro": "No tienes que forzar nada. Solo vamos a bajar un poco la velocidad del cuerpo.",
        "steps": [
            "Inhala suavemente durante 4 segundos.",
            "Mantén la respiración de forma ligera durante 2 segundos.",
            "Exhala durante 6 segundos, como si empañaras un espejo.",
            "Repite 5 veces y luego deja que la respiración vuelva a su ritmo natural."
        ]
    },
    "Quiero revisar el teléfono": {
        "title": "📵 Redirección anti-scroll",
        "intro": "Revisar el teléfono le dice al cerebro que ya es de día. Este es tu punto de pausa.",
        "steps": [
            "Pon el teléfono boca abajo o lejos de la cama.",
            "No revises mensajes, noticias, correo ni la hora otra vez.",
            "Elige una imagen mental aburrida: un cuarto oscuro, un tren lento o niebla sobre el mar.",
            "Quédate con esa imagen durante 2 minutos."
        ]
    },
    "Me frustra estar despierto": {
        "title": "🪨 Reinicio de aceptación",
        "intro": "Pelear con el insomnio suele despertar más al cerebro. Vamos a ir a un punto neutral.",
        "steps": [
            "Di: no tengo que dormir perfecto para descansar.",
            "Relaja la frente y la mandíbula.",
            "Deja que la cama sostenga todo tu peso.",
            "Repite: descansar es suficiente por ahora."
        ]
    },
    "Me siento demasiado despierto": {
        "title": "🌘 Modo aburrido",
        "intro": "La meta no es entretenerte. La meta es aburrir suavemente al cerebro.",
        "steps": [
            "Cuenta hacia atrás desde 300 de 3 en 3 lentamente.",
            "Si pierdes la cuenta, vuelve con calma al 300.",
            "Mantén los ojos cerrados o medio cerrados.",
            "Haz que cada número se sienta más silencioso que el anterior."
        ]
    }
}

st.title("🌙 Rescate 4AM")
st.subheader("Una app tranquila para ayudarte a volver a dormir")
st.markdown("<p class='small-note'>Primera regla: no hacer scroll, no revisar mensajes, no resolver problemas.</p>", unsafe_allow_html=True)

if st.button("Me desperté y quiero volver a dormir"):
    st.session_state.wake_log.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
    st.success(random.choice(messages))

st.divider()

st.header("¿Qué está pasando ahora mismo?")
choice = st.radio(
    "Elige la opción más cercana:",
    list(activities.keys()),
    index=None
)

if choice:
    activity = activities[choice]
    st.markdown(f"<div class='calm-card'><h3>{activity['title']}</h3><p>{activity['intro']}</p></div>", unsafe_allow_html=True)
    for i, step in enumerate(activity["steps"], start=1):
        st.write(f"**{i}.** {step}")

    if st.button("Ya hice esta actividad"):
        st.session_state.activity_done.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "activity": activity["title"]
        })
        st.success("Bien. Ahora deja el teléfono y permite que tu cuerpo se vuelva pesado.")

st.divider()

st.header("Estaciona el pensamiento")
st.write("Escríbelo una vez. No tienes que resolverlo esta noche.")
thought = st.text_area("¿Qué está intentando traer tu mente?", height=100)

if st.button("Guardar este pensamiento hasta mañana"):
    if thought.strip():
        st.session_state.parked_thoughts.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "thought": thought.strip()
        })
        st.success("Guardado. No tienes que cargar con esto ahora.")
    else:
        st.info("Está bien. No tienes que escribir nada si no quieres.")

st.divider()

st.header("Escaneo corporal")
st.write("""
Suaviza los ojos.  
Relaja la mandíbula.  
Suelta los hombros.  
Afloja las manos.  
Deja que el estómago se relaje.  
Permite que las piernas se sientan pesadas.  

Imagina que tu cuerpo ya está dormido y que tu mente solo está alcanzándolo.
""")

st.divider()
st.header("Sonidos para acompañar el sueño")
st.write("Elige una sola opción directa. No hay que buscar, comparar ni decidir entre videos.")

st.markdown("""
<div class='calm-card'>
<h3>🌙 Opción recomendada</h3>
<p>Para no pensar: abre este sonido, baja el brillo, baja el volumen y deja el teléfono a un lado.</p>
</div>
""", unsafe_allow_html=True)

st.link_button(
    "▶️ No quiero pensar, pon sonido para dormir",
    "https://www.youtube.com/watch?v=nMfPqeZjc2c",
    use_container_width=True
)

st.info("🌙 Modo sin interrupciones: si usas YouTube Premium, estos sonidos pueden reproducirse sin anuncios, lo que ayuda a mantener una experiencia tranquila sin estímulos inesperados durante la noche.")

st.caption("También estamos considerando una versión futura con audios internos sin depender de YouTube, ideal para una experiencia más controlada y completamente enfocada en volver a dormir.")

st.subheader("YouTube")
st.caption("Videos directos para abrir una opción específica sin tener que buscar.")

youtube_sound_links = {
    "🌧️ Lluvia suave": "https://www.youtube.com/watch?v=mPZkdNFkNps",
    "🌊 Olas del mar": "https://www.youtube.com/watch?v=bn9F19Hi1Lk",
    "🤍 Ruido blanco": "https://www.youtube.com/watch?v=nMfPqeZjc2c",
    "🟤 Brown noise": "https://www.youtube.com/watch?v=Q6MemVxEquE",
    "🌀 Ventilador": "https://www.youtube.com/watch?v=C5Gm8UvxKlU",
    "🌲 Bosque nocturno": "https://www.youtube.com/watch?v=xNN7iTA57jM",
}

cols = st.columns(2)

for i, (label, url) in enumerate(youtube_sound_links.items()):
    with cols[i % 2]:
        st.link_button(label, url, use_container_width=True)

st.caption("Tip: no leas comentarios, no cambies de video y no abras más pestañas.")

st.markdown("""
<div class='calm-card'>
<h3>🎧 Spotify</h3>
<p>Si prefieres audio sin video, abre una opción equivalente en Spotify. Ideal si ya usas Spotify para dormir.</p>
</div>
""", unsafe_allow_html=True)

st.caption("En Spotify también puede haber anuncios si usas la versión gratis. Spotify Premium ayuda a mantener la experiencia sin interrupciones.")

spotify_sound_links = {
    "🌧️ Lluvia suave en Spotify": "https://open.spotify.com/search/rain%20sounds%20sleep",
    "🌊 Olas del mar en Spotify": "https://open.spotify.com/search/ocean%20waves%20sleep",
    "🤍 Ruido blanco en Spotify": "https://open.spotify.com/search/white%20noise%20sleep",
    "🟤 Brown noise en Spotify": "https://open.spotify.com/search/brown%20noise%20sleep",
    "🌀 Ventilador en Spotify": "https://open.spotify.com/search/fan%20noise%20sleep",
    "🌲 Bosque nocturno en Spotify": "https://open.spotify.com/search/forest%20night%20sounds%20sleep",
}

spotify_cols = st.columns(2)

for i, (label, url) in enumerate(spotify_sound_links.items()):
    with spotify_cols[i % 2]:
        st.link_button(label, url, use_container_width=True)

st.caption("Tip: elige una sola opción, pon temporizador si lo necesitas y no sigas buscando más sonidos.")
st.divider()

with st.expander("Revisión por la mañana"):
    st.write("Despertares registrados:")
    if st.session_state.wake_log:
        for item in st.session_state.wake_log:
            st.write("🌙", item)
    else:
        st.write("Todavía no hay despertares registrados.")

    st.write("Actividades completadas:")
    if st.session_state.activity_done:
        for item in st.session_state.activity_done:
            st.write(f"{item['time']} — {item['activity']}")
    else:
        st.write("Todavía no hay actividades completadas.")

    st.write("Pensamientos guardados:")
    if st.session_state.parked_thoughts:
        for item in st.session_state.parked_thoughts:
            st.write(f"{item['time']} — {item['thought']}")
    else:
        st.write("Todavía no hay pensamientos guardados.")
