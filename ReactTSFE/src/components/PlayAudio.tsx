import type React from "react";
import { useState } from "react";
import axios from "axios";
import styles from "./FncButtons.module.css";

type PlayAudioType = {
  audio_type: string;
  lang_code: string;
};

const PlayAudio: React.FC<PlayAudioType> = ({ audio_type, lang_code }) => {
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("");
  const playAudio = async () => {
    try {
      setRunning(true);
      setStatus("Playing audio ...");
      const response = await axios.post(
        "http://localhost:8000/play_audio",
        {
          audio_type: audio_type,
          lang_code: lang_code,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      setStatus(response.data.message || "Audio played");
    } catch (err) {
      console.error(err);
      setStatus("Failed to play audio");
    } finally {
      setRunning(false);
    }
  };
  return (
    <div>
      <button
        className={styles.fncButton}
        onClick={playAudio}
        disabled={running}
      >
        ▶
      </button>
      <p>{status}</p>
    </div>
  );
};

export default PlayAudio;
