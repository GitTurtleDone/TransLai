import { useState } from "react";
import TranslatorBox from "./components/TranslatorBox";
import languages from "./data/languages.json";
import RecordTemplateButton from "./components/RecordTemplateButton";
import TranslateButton from "./components/RecordTranslationButton";
import StopNTranslateButton from "./components/StopNTranslateButton";
import StopRecordingTemplateButton from "./components/StopRecordingTemplateButton";
// import { FileX } from "lucide-react";

// const
// // languages = [
// //   { code: "en", name: "English" },
// //   { code: "vi", name: "Vietnamese" },
// //   { code: "fr", name: "French" },
// //   { code: "es", name: "Spanish" },
// // ];

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
      <h1>Portable Translator</h1>
      <RecordTemplateButton />
      <StopRecordingTemplateButton />
      <div
        style={{
          display: "flex",
          width: "80%",
          gap: "2rem",
          flexWrap: "wrap",
          justifyContent: "left",
          marginBottom: "2rem",
          marginTop: "1rem",
          // alignItems: "left",

          // border: "1px solid gray", // visual aid
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
      <TranslateButton ipt_lang_code={inputLang} opt_lang_code={outputLang} />
      <StopNTranslateButton/>
    </div>
  );
}

export default App;
