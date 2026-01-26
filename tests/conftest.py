import pytest

@pytest.fixture
def sample_park_html():
    return """
    <html>
        <body>
            <div data-testid="trail-card">
                <a data-testid="trail-card-title-link" href="/trail/us/tennessee/alum-cave">Alum Cave Trail</a>
                <span class="difficulty">Hard</span>
                <p data-testid="trail-card-description">A beautiful trail with caves and views.</p>
                <div>Length: 5.0 mi • 4.8 stars</div>
            </div>
            <div data-testid="trail-card">
                <a data-testid="trail-card-title-link" href="/trail/us/tennessee/chimney-tops">Chimney Tops</a>
                <span class="difficulty">Moderate</span>
                <p data-testid="trail-card-description">Steep climb to rock formations.</p>
                <div>Length: 3.5 mi • 4.5 stars</div>
            </div>
        </body>
    </html>
    """

@pytest.fixture
def sample_trail_html():
    return """
    <html>
        <body>
            <h1 data-testid="trail-title">Alum Cave Trail to Mount LeConte</h1>
            <div data-testid="trail-description">
                A challenging but rewarding hike to one of the highest peaks in the Smokies.
                Features interesting rock formations and panoramic views.
            </div>
            <div data-testid="trail-length">11.0 mi</div>
            <div data-testid="trail-elevation">2,763 ft</div>
            <div data-testid="trail-difficulty">Hard</div>
            <div data-testid="trail-rating">4.8</div>
            <div>Route type: Out & back</div>
        </body>
    </html>
    """
