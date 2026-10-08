import { useState } from "react";

function TravelForm({ onSubmit, loading }) {
  const [request, setRequest] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!request.trim()) {
      return;
    }

    onSubmit(request.trim());
  };

  return (
    <form
      className="travel-form"
      onSubmit={handleSubmit}
    >
      <textarea
        value={request}
        onChange={(e) => setRequest(e.target.value)}
        placeholder="Example: I want to visit Dubai for 5 days in December with a $500 budget"
        disabled={loading}
        rows={4}
      />

      <button
        type="submit"
        disabled={loading || !request.trim()}
      >
        {loading
          ? "🤖 AI is planning..."
          : "✈️ Plan My Trip"}
      </button>
    </form>
  );
}

export default TravelForm;