import { useEffect, useRef, useState } from "react";

function PlanningProgress({ messages, isPlanning }) {
  const [expanded, setExpanded] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (expanded) {
      messagesEndRef.current?.scrollIntoView({
        behavior: "smooth",
      });
    }
  }, [messages, expanded]);

  if (messages.length === 0) {
    return null;
  }

  const latestMessage = messages[messages.length - 1];

  return (
    <div className="planning-progress">

      <button
        className="progress-header"
        onClick={() => setExpanded((previous) => !previous)}
        type="button"
      >
        <div className="progress-title">

          {isPlanning ? (
            <span className="loading-dot"></span>
          ) : (
            <span className="completed-dot">✓</span>
          )}

          <span>
            {isPlanning
              ? latestMessage
              : "Trip planning completed"}
          </span>
        </div>

        <span className="progress-arrow">
          {expanded ? "▲" : "▼"}
        </span>
      </button>

      {expanded && (
        <div className="progress-messages">

          {messages.map((message, index) => {
            const isLatest =
              index === messages.length - 1;

            return (
              <div
                key={`${message}-${index}`}
                className={`progress-message ${
                  isLatest && isPlanning
                    ? "active-message"
                    : ""
                }`}
              >
                <span className="message-check">
                  {isLatest && isPlanning ? "●" : "✓"}
                </span>

                <span>{message}</span>
              </div>
            );
          })}

          <div ref={messagesEndRef} />

        </div>
      )}

    </div>
  );
}

export default PlanningProgress;