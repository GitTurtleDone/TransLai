import type React from "react";
import { useState } from "react";
import axios from "axios";
import styles from "./FncButtons.module.css";

interface Props {
  setInputText: (text: string) => void;
  setOutputText: (text: string) => void;
}
const StopNTranslateButton: React.FC = ({setInputText, setOutputText}: Props) => {
  const [status, setStatus] = useState("");
  const [running, setRunning] = useState(false);
  const stopNTranslate = async () => {
    try {
      setRunning(true);
      setStatus("Translating ...");
      const response = await axios.post(
        "http://localhost:8000/stop_n_translate",
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log(response.data.message || "Translated.");
      setInputText(response.data.ipt_txt);
      setOutputText(response.data.opt_txt);
    } catch (err) {
      setStatus("Failed to Stop and TransLate");
      console.error(err);
    } finally {
      setStatus("Stop and Translate completed.");
      setRunning(false);
    }
  };
  return (
    <div>
      <button
        className={styles.fncButton}
        onClick={stopNTranslate}
        disabled={running}
      >Stop and Translate</button>
      <p>{status}</p>
    </div>
  );
};
export default StopNTranslateButton;
