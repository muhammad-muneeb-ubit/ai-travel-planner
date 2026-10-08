import { useState } from "react";
import TravelForm from "./components/TravelForm";
import PlanningProgress from "./components/PlanningProgress";
import TravelPlan from "./components/TravelPlan";
import "./App.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");
  const [isPlanning, setIsPlanning] = useState(false);
  const [userPrompt, setUserPrompt] = useState("");

  const startPlanning = async (request) => {
    setLoading(true);
    setIsPlanning(true);

    setMessages([]);
    setPlan(null);
    setError("");
    setUserPrompt(request);

    try {
      const url =
        `http://127.0.0.1:3000/api/plan/stream?request=` +
        encodeURIComponent(request);

      console.log("Request URL:", url);

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}`
        );
      }

      if (!response.body) {
        throw new Error(
          "The server did not return a streaming response."
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        const events = buffer.split("\n\n");

        buffer = events.pop() || "";

        for (const event of events) {
          if (!event.startsWith("data:")) {
            continue;
          }

          const jsonString = event
            .replace(/^data:\s*/, "")
            .trim();

          if (!jsonString) {
            continue;
          }

          try {
            const data = JSON.parse(jsonString);

            console.log("SSE event:", data);

            /*
             * START
             */
            if (data.type === "start") {
              setMessages((previous) => [
                ...previous,
                data.message,
              ]);
            }

            /*
             * PROGRESS
             */
            else if (data.type === "progress") {
              setMessages((previous) => [
                ...previous,
                data.message,
              ]);
            }

            /*
             * COMPLETE
             */
            else if (data.type === "complete") {
              setMessages((previous) => [
                ...previous,
                data.message || "Trip planned successfully.",
              ]);

              setPlan(data.plan);

              setIsPlanning(false);
              setLoading(false);
            }

            /*
             * ERROR
             */
            else if (data.type === "error") {
              setMessages((previous) => [
                ...previous,
                `❌ ${data.message}`,
              ]);

              setError(
                data.message ||
                  "Something went wrong while planning your trip."
              );

              setIsPlanning(false);
              setLoading(false);
            }
          } catch (parseError) {
            console.error(
              "Invalid SSE event:",
              jsonString,
              parseError
            );
          }
        }
      }
    } catch (error) {
      console.error("Planning error:", error);

      const readableError = getReadableError(error);

      setError(readableError);

      setMessages((previous) => [
        ...previous,
        `❌ ${readableError}`,
      ]);

      setIsPlanning(false);
    } finally {
      setLoading(false);
      setIsPlanning(false);
    }
  };

  function getReadableError(error) {
    if (
      error instanceof TypeError &&
      error.message === "Failed to fetch"
    ) {
      return "Unable to connect to the travel planner. Please make sure the backend is running.";
    }

    if (error.name === "AbortError") {
      return "The request was cancelled. Please try again.";
    }

    if (error.message?.includes("CORS")) {
      return "The server blocked the request. Please check the backend CORS configuration.";
    }

    if (error.message?.includes("500")) {
      return "The travel planner encountered a server error. Please try again.";
    }

    return (
      error.message ||
      "Something went wrong while planning your trip."
    );
  }

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">

        <div className="logo">
          ✈️ AI Travel Planner
        </div>

        <div className="subtitle">
          ✨ AI POWERED
        </div>

      </header>


      <main className="container">

        {/* =========================
            INITIAL FORM
        ========================== */}

        {!loading && !plan && messages.length === 0 && (
          <section className="hero">

            <h1>
              Where do you want to go?
            </h1>

            <p>
              Tell our AI planner about your trip and
              we'll find the best combination of flights,
              hotels and activities.
            </p>

            <TravelForm
              onSubmit={startPlanning}
              loading={loading}
            />

          </section>
        )}


        {/* =========================
            PLANNING / RESULT PAGE
        ========================== */}

        {(loading || messages.length > 0 || plan) && (
          <div className="result-page">

            {/* USER REQUEST */}

            <div className="user-request">

              <div className="request-label">
                Your request
              </div>

              <div className="request-text">
                {userPrompt}
              </div>

            </div>


            {/* LIVE PROGRESS */}

            <PlanningProgress
              messages={messages}
              isPlanning={isPlanning}
            />


            {/* FINAL PLAN */}

            {plan && !loading && (
              <TravelPlan
                plan={plan}
                onNewTrip={() => {
                  setPlan(null);
                  setMessages([]);
                  setUserPrompt("");
                  setError("");
                  setIsPlanning(false);
                  setLoading(false);
                }}
              />
            )}

          </div>
        )}


        {/* ERROR */}

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

      </main>

    </div>
  );
}

export default App;

