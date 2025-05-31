import { useState } from "react";
import TranslatorBox from "./components/TranslatorBox";
import languages from "./data/languages.json";
import RecordTemplateButton from "./components/RecordTemplate";
import RecordTranslationButton from "./components/RecordTranslationButton";
import StopNTranslateButton from "./components/StopNTranslateButton";
import StopRecordingTemplateButton from "./components/StopRecordingTemplateButton";
import styles from "./components/FncButtons.module.css";
function App() {
  const [inputLang, setInputLang] = useState("en");
  const [inputText, setInputText] = useState("");
  const [outputLang, setOutputLang] = useState("vi");
  const [outputText, setOutputText] = useState("");

  return (
    <div
      style={{
        width: "100vw",
        display: "flex",
        flexDirection: "column",
        alignItems: "left",
        boxSizing: "border-box",
        padding: "2rem",
      }}
    >
      <h1>Off-line Translator</h1>
      <RecordTemplateButton />
      <div
        style={{
          display: "flex",
          width: "80%",
          gap: "2rem",
          flexWrap: "wrap",
          justifyContent: "left",
          marginBottom: "2rem",
          marginTop: "1rem",
        }}
      >
        <TranslatorBox
          label="Input"
          language={inputLang}
          setLanguage={setInputLang}
          text={inputText}
          setText={setInputText}
          languages={languages}
        />
        <TranslatorBox
          label="Output"
          language={outputLang}
          setLanguage={setOutputLang}
          text={outputText}
          setText={setOutputText}
          languages={languages}
        />
      </div>
      <div className={styles.container}>
        <RecordTranslationButton
          ipt_lang_code={inputLang}
          opt_lang_code={outputLang}
        />
        <StopNTranslateButton
          setInputText={setInputText}
          setOutputText={setOutputText}
        />
      </div>
    </div>
  );
}

export default App;
