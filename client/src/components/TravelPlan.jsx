function TravelPlan({ plan, onNewTrip }) {
  const budget = Number(
    String(plan.budget)
      .replace("$", "")
      .replace(",", "")
  );

  const total = Number(plan.total_cost);

  const remaining =
    plan.remaining_budget !== undefined
      ? Number(plan.remaining_budget)
      : budget - total;

  return (
    <section className="plan-section">

      <div className="plan-header">
        <div>
          <span className="success-label">
            ✓ TRIP PLANNED
          </span>

          <h1 style={{ color: remaining < 0 ? "red" : "inherit" }}>
            Your {plan.destination} Trip
          </h1>

          <p>
            {plan.days} days • {plan.month}
          </p>
        </div>

        <button
          className="new-trip-button"
          onClick={onNewTrip}
        >
          + New Trip
        </button>
      </div>

      <div className="plan-grid">

        {/* Flight */}
        <div className="plan-card">

          <div className="card-title">
            ✈️
            <span>Flight</span>
          </div>

          <h3>
            {plan.flight?.airline}
          </h3>

          <p>
            {plan.flight?.from}
            {" → "}
            {plan.flight?.to}
          </p>

          <div className="card-price">
            ${plan.flight?.price}
          </div>

          <small>
            {plan.flight?.duration_hours} hours
          </small>

        </div>


        {/* Hotel */}
        <div className="plan-card">

          <div className="card-title">
            🏨
            <span>Hotel</span>
          </div>

          <h3>
            {plan.hotel?.name}
          </h3>

          <p>
            {plan.hotel?.location}
          </p>

          <p>
            {"⭐".repeat(plan.hotel?.rating || 0)}
          </p>

          <div className="card-price">
            ${plan.hotel?.price_per_night}
            <small>/night</small>
          </div>

        </div>


        {/* Activities */}
        <div className="plan-card activities-card">

          <div className="card-title">
            🎯
            <span>Activities</span>
          </div>

          {plan.activities?.length > 0 ? (
            plan.activities.map((activity) => (
              <div
                className="activity"
                key={activity.id}
              >
                <div>
                  <strong>
                    {activity.name}
                  </strong>

                  <small>
                    {activity.category}
                  </small>
                </div>

                <span>
                  ${activity.price}
                </span>
              </div>
            ))
          ) : (
            <p>No activities selected.</p>
          )}

        </div>

      </div>


      {/* Budget */}
      <div className="budget-card">

        <div>
          <span>
            💰 Total Trip Cost
          </span>

          <h2 style={{ color: remaining < 0 ? "red" : "inherit" }}>
            ${total}
          </h2>
        </div>

        <div className="budget-info">

          <span>
            Budget: ${budget}
          </span>

          {remaining >= 0 ? (
            <span className="budget-good">
              ✓ ${remaining} remaining
            </span>
          ) : (
            <span className="budget-warning">
              ⚠️ ${Math.abs(remaining)} over budget
            </span>
          )}

        </div>

      </div>

    </section>
  );
}

export default TravelPlan;