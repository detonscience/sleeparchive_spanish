import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import random
import base64
from pathlib import Path

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
/* Fix Streamlit selectbox/dropdown colors in dark mode */
div[data-baseweb="select"] > div {
    background-color: #15152a !important;
    color: #ffffff !important;
    border: 1px solid #6b6bb0 !important;
    border-radius: 14px !important;
}
div[data-baseweb="select"] input {
    color: #ffffff !important;
    caret-color: #ffffff !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Streamlit/BaseWeb renders the dropdown menu in a floating portal, so target it globally too */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"],
div[role="listbox"] {
    background-color: #15152a !important;
    color: #ffffff !important;
    border: 1px solid #6b6bb0 !important;
}
ul[role="listbox"] li,
div[role="option"],
li[role="option"] {
    background-color: #15152a !important;
    color: #ffffff !important;
}
ul[role="listbox"] li *,
div[role="option"] *,
li[role="option"] * {
    color: #ffffff !important;
    font-weight: 800 !important;
}
ul[role="listbox"] li:hover,
div[role="option"]:hover,
li[role="option"]:hover {
    background-color: #303060 !important;
    color: #ffffff !important;
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
.player-note {
    opacity: 0.82;
    font-size: 0.92rem;
    margin-top: -0.4rem;
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

def render_one_click_audio_player(title, file_path):
    audio_path = Path(file_path)

    if not audio_path.exists():
        st.warning(f"Falta el archivo local: {file_path}")
        return

    audio_bytes = audio_path.read_bytes()
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

    components.html(
        f"""
        <div style="margin: 0.4rem 0 0.8rem 0;">
            <button
                onclick="
                    const audios = window.parent.document.querySelectorAll('audio');
                    audios.forEach(a => {{ a.pause(); a.currentTime = 0; }});
                    const audio = document.getElementById('{audio_path.stem}');
                    audio.loop = true;
                    audio.volume = 0.55;
                    audio.play();
                "
                style="
                    width: 100%;
                    background-color: #24244a;
                    color: #ffffff;
                    border-radius: 18px;
                    border: 1px solid #6b6bb0;
                    padding: 0.9rem 1rem;
                    font-size: 17px;
                    font-weight: 700;
                    cursor: pointer;
                "
            >
                ▶️ {title}
            </button>
            <audio id="{audio_path.stem}" preload="auto">
                <source src="data:audio/mpeg;base64,{encoded_audio}" type="audio/mpeg">
            </audio>
        </div>
        """,
        height=80,
    )


def render_youtube_embed(title, video_id):
    st.markdown(f"**{title}**")
    components.html(
        f"""
        <iframe
            width="100%"
            height="170"
            src="https://www.youtube.com/embed/{video_id}?autoplay=0&controls=1&rel=0&modestbranding=1&playsinline=1&loop=1&playlist={video_id}"
            title="{title}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen>
        </iframe>
        """,
        height=190,
    )


def render_spotify_embed(title, spotify_playlist_id):
    st.markdown(f"**{title}**")
    components.html(
        f"""
        <iframe
            style="border-radius:12px"
            src="https://open.spotify.com/embed/playlist/{spotify_playlist_id}?utm_source=generator&theme=0"
            width="100%"
            height="152"
            frameborder="0"
            allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy">
        </iframe>
        """,
        height=172,
    )

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

st.markdown("""
<div class='calm-card'>
<h3>🔊 Reproductor interno de un solo clic</h3>
<p>Esta es la mejor opción para la madrugada: das un clic y el sonido empieza dentro de la app. No hay que abrir YouTube, Spotify ni buscar el botón de play.</p>
<p>Los audios se repiten en loop continuo, así que pueden acompañar por 6 horas o más si el teléfono no bloquea el navegador.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Para activar esta parte, coloca archivos .mp3 en una carpeta llamada audio junto a este archivo de Python. Ejemplo: audio/ruido_blanco.mp3")

local_audio_links = {
    "No quiero pensar: ruido blanco continuo": "audio/ruido_blanco.mp3",
    "Lluvia suave continua": "audio/lluvia_suave.mp3",
    "Olas del mar continuas": "audio/olas_mar.mp3",
    "Brown noise continuo": "audio/brown_noise.mp3",
    "Ventilador continuo": "audio/ventilador.mp3",
    "Bosque nocturno continuo": "audio/bosque_nocturno.mp3",
}

for audio_label, audio_file in local_audio_links.items():
    render_one_click_audio_player(audio_label, audio_file)

st.caption("YouTube y Spotify siguen disponibles como respaldo, pero por reglas de navegador y de esas plataformas puede que pidan otro toque para reproducir.")

st.subheader("Mini players dentro de la app")
st.info("Los mini players evitan abrir otra página. Por reglas de navegador, YouTube y Spotify pueden requerir tocar play dentro del player, pero el usuario ya no tiene que buscar ni escoger nada.")

st.subheader("YouTube embebido")
st.caption("Videos directos dentro de la app. Procura usar videos de 6 horas o más.")

youtube_embed_links = {
    "🌧️ Lluvia suave": "mPZkdNFkNps",
    "🌊 Olas del mar": "bn9F19Hi1Lk",
    "🤍 Ruido blanco": "nMfPqeZjc2c",
    "🟤 Brown noise": "Q6MemVxEquE",
    "🌀 Ventilador": "C5Gm8UvxKlU",
    "🌲 Bosque nocturno": "xNN7iTA57jM",
}

selected_youtube = st.selectbox(
    "YouTube: sonido ya escogido",
    list(youtube_embed_links.keys()),
    index=2
)
render_youtube_embed(selected_youtube, youtube_embed_links[selected_youtube])

st.caption("Tip: toca play una vez, no leas comentarios, no cambies de video y no abras más pestañas.")

st.markdown("""
<div class='calm-card'>
<h3>🎧 Spotify</h3>
<p>Si prefieres audio sin video, abre una opción equivalente en Spotify. Ideal si ya usas Spotify para dormir.</p>
</div>
""", unsafe_allow_html=True)

spotify_embed_links = {
    "🌧️ Lluvia suave en Spotify": "37i9dQZF1DXdp5bwJ1FHFe",
    "🌊 Olas del mar en Spotify": "37i9dQZF1DX9if5QDLdzCa",
    "🤍 Ruido blanco en Spotify": "37i9dQZF1DWUZ5bk6qqDSy",
    "🟤 Brown noise en Spotify": "37i9dQZF1DX4hpot8sYudB",
    "🌀 Ventilador en Spotify": "37i9dQZF1DWUm4vT7WQxcD",
    "🌲 Bosque nocturno en Spotify": "37i9dQZF1DWWSads6V2oIk",
}

selected_spotify = st.selectbox(
    "Spotify: playlist ya escogida",
    list(spotify_embed_links.keys()),
    index=2
)
render_spotify_embed(selected_spotify, spotify_embed_links[selected_spotify])

st.caption("Tip: toca play una vez, pon temporizador si lo necesitas y no sigas buscando más sonidos.")
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
