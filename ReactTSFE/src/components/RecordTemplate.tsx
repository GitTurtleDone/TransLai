import type React from "react";
import { useState } from "react";
import axios from "axios";
import languages from "../data/languages.json";
import styles from "./FncButtons.module.css";
import StopRecordingTemplateButton from "./StopRecordingTemplateButton";
import PlayAudio from "./PlayAudio";

const RecordTemplate: React.FC = () => {
  const [lang, setLang] = useState("en");
  const [status, setStatus] = useState("");
  const [running, setRunning] = useState(false);
  const record = async () => {
    try {
      setRunning(true);
      setStatus("Recording ... Wait about 3 s after that speak clearly");
      const response = await axios.post(
        "http://localhost:8000/record_template",
        {
          lang_code: lang,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      setStatus(response.data.message || "Record completed");
    } catch (err) {
      console.error(err);
      setStatus("Failed to record");
    } finally {
      setRunning(false);
    }
  };
  return (
    <div className={styles.container}>
      <div className={styles.item}>
        <div className={styles.container}>
          <button
            className={styles.fncButton}
            onClick={record}
            disabled={running}
          >
            Record Template Voice
          </button>
          <div className={styles.item}>
            <select
              style={{ marginLeft: "2rem" }}
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              disabled={running}
            >
              {languages.map((language) => (
                <option key={language.code} value={language.code}>
                  {language.name}
                </option>
              ))}
              ;
            </select>
          </div>
        </div>
        <p>{status}</p>
        {/* <p style={{ maxWidth: "20rem", wordBreak: "break-word" }}>{status}</p> */}
        {/* <p style={{max-width: "5rem"}}>{status}</p> */}
      </div>
      <div className={styles.item}></div>
      <div className={styles.item}>
        <StopRecordingTemplateButton />
      </div>

      <div className={styles.item}>
        <PlayAudio audio_type="template" lang_code={lang} />
      </div>
    </div>
  );
};

export default RecordTemplate;
