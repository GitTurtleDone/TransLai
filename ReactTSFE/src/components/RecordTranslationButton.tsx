import type React from "react";
import { useState } from "react";
import axios from "axios";
import styles from "./FncButtons.module.css";
type languages = {
  ipt_lang_code: string;
  opt_lang_code: string;
};
const RecordTranslationButton: React.FC<languages> = ({
  ipt_lang_code,
  opt_lang_code,
}) => {
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("");
  const recordTranslation = async () => {
    try {
      setRunning(true);
      setStatus("Recording for translation ...");
      const response = await axios.post(
        "http://localhost:8000/record_translation",
        {
          ipt_lang_code: ipt_lang_code,
          opt_lang_code: opt_lang_code,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      setStatus(response.data.message || "Translation speech is being recorded");
    } catch (err) {
      console.error(err);
      setStatus("Failed to record translation");
    } finally {
      setRunning(false);
    }
  };
  return (
    <div>
      <button
        className={styles.fncButton}
        onClick={recordTranslation}
        disabled={running}
      >
        Record Translation
      </button>
      <p>{status}</p>
    </div>
  );
};

export default RecordTranslationButton;
