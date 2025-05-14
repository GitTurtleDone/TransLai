import { useState } from "react";
import TranslatorBox from "./components/TranslatorBox";
import languages from "./data/languages.json";
import { FileX } from "lucide-react";

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
        alignItems: "center",
        boxSizing: "border-box",
      }}
    >
      <h1>Portable Translator</h1>
      <div
        style={{
          display: "flex",
          width: "80%",
          gap: "2rem",
          flexWrap: "wrap",
          justifyContent: "center",
          border: "1px solid gray", // visual aid
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
    </div>
  );
}

export default App;
