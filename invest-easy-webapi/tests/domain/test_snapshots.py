import pytest
from datetime import datetime
from app.domain.snapshots import Snapshots
import uuid


class TestSnapshots:
    """Test cases for Snapshots domain class."""

    @pytest.fixture
    def snapshot_instance(self):
        """Create a basic Snapshots instance for testing."""
        return Snapshots(
            instrument_id=uuid.uuid4(),
            market="US",
            code="US.AAPL",
            futu_code="US.AAPL",
            name_cn="Apple Inc"
        )

    def test_upsert_no_changes(self, snapshot_instance):
        """Test upsert method when no fields change."""
        initial_updated_at = snapshot_instance.updated_at
        initial_price = 150.0
        snapshot_instance.latest_price = initial_price
        
        # Create a record with the same values
        record = {"latest_price": initial_price}
        
        # Call upsert - should not change anything
        snapshot_instance.upsert(record)
        
        # Verify no changes occurred
        assert snapshot_instance.latest_price == initial_price
        assert snapshot_instance.updated_at == initial_updated_at

    def test_upsert_with_changes(self, snapshot_instance):
        """Test upsert method when fields change."""
        initial_updated_at = snapshot_instance.updated_at
        old_price = 150.0
        new_price = 155.0
        snapshot_instance.latest_price = old_price
        
        # Create a record with new values
        record = {"latest_price": new_price}
        
        # Call upsert - should update the field and timestamp
        snapshot_instance.upsert(record)
        
        # Verify changes occurred
        assert snapshot_instance.latest_price == new_price
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_upsert_multiple_fields(self, snapshot_instance):
        """Test upsert method with multiple field changes."""
        initial_updated_at = snapshot_instance.updated_at
        
        # Set initial values
        snapshot_instance.latest_price = 150.0
        snapshot_instance.change_percent = 1.0
        snapshot_instance.volume = 1000.0
        
        # Create a record with multiple new values
        record = {
            "latest_price": 155.0,
            "change_percent": 2.0,
            "volume": 1500.0,
            "market_cap": 1000000.0
        }
        
        # Call upsert
        snapshot_instance.upsert(record)
        
        # Verify all changes occurred
        assert snapshot_instance.latest_price == 155.0
        assert snapshot_instance.change_percent == 2.0
        assert snapshot_instance.volume == 1500.0
        assert snapshot_instance.market_cap == 1000000.0
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_upsert_ignore_nonexistent_fields(self, snapshot_instance):
        """Test upsert method ignores fields that don't exist on the model."""
        initial_updated_at = snapshot_instance.updated_at
        
        # Create a record with both existing and non-existing fields
        record = {
            "latest_price": 155.0,  # exists
            "nonexistent_field": "value",  # doesn't exist
            "change_percent": 2.0  # exists
        }
        
        # Call upsert
        snapshot_instance.upsert(record)
        
        # Verify only existing fields were updated
        assert snapshot_instance.latest_price == 155.0
        assert snapshot_instance.change_percent == 2.0
        assert not hasattr(snapshot_instance, "nonexistent_field")
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_upsert_format_na_values(self, snapshot_instance):
        """Test upsert method formats 'N/A' values to None."""
        initial_updated_at = snapshot_instance.updated_at
        
        # Create a record with N/A values
        record = {
            "latest_price": "N/A",
            "change_percent": 1.0,
            "pe_ratio": "N/A"
        }
        
        # Call upsert
        snapshot_instance.upsert(record)
        
        # Verify N/A values were converted to None
        assert snapshot_instance.latest_price is None
        assert snapshot_instance.change_percent == 1.0
        assert snapshot_instance.pe_ratio is None
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_upsert_format_nan_values(self, snapshot_instance):
        """Test upsert method formats 'NaN' values to None."""
        initial_updated_at = snapshot_instance.updated_at
        
        # Create a record with NaN values
        record = {
            "latest_price": "NaN",
            "change_percent": 2.0,
            "volume": "NaN"
        }
        
        # Call upsert
        snapshot_instance.upsert(record)
        
        # Verify NaN values were converted to None
        assert snapshot_instance.latest_price is None
        assert snapshot_instance.change_percent == 2.0
        assert snapshot_instance.volume is None
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_upsert_no_changes_no_timestamp_update(self, snapshot_instance):
        """Test that timestamp is not updated when no actual changes occur."""
        initial_updated_at = snapshot_instance.updated_at
        snapshot_instance.latest_price = 150.0
        
        # Create a record with the same values
        record = {"latest_price": 150.0}
        
        # Call upsert - should not update timestamp
        snapshot_instance.upsert(record)
        
        # Verify timestamp was not updated
        assert snapshot_instance.updated_at == initial_updated_at

    def test_upsert_mixed_changes(self, snapshot_instance):
        """Test upsert method with mix of changed, unchanged, and None values."""
        initial_updated_at = snapshot_instance.updated_at
        snapshot_instance.latest_price = 150.0
        snapshot_instance.change_percent = 1.0
        
        # Create a record with mixed values
        record = {
            "latest_price": 150.0,  # same value - no change
            "change_percent": 2.0,  # different value - should change
            "volume": None,         # None value - should set to None
            "market_cap": 1000000.0 # new field - should set
        }
        
        # Call upsert
        snapshot_instance.upsert(record)
        
        # Verify results
        assert snapshot_instance.latest_price == 150.0  # unchanged
        assert snapshot_instance.change_percent == 2.0   # changed
        assert snapshot_instance.volume is None          # set to None
        assert snapshot_instance.market_cap == 1000000.0 # new value set
        if initial_updated_at is None:
            assert snapshot_instance.updated_at is not None
        else:
            assert snapshot_instance.updated_at > initial_updated_at

    def test_format_value_method_directly(self, snapshot_instance):
        """Test the _format_value method directly."""
        # Test N/A formatting
        assert snapshot_instance._format_value("field", "N/A") is None
        
        # Test NaN formatting
        assert snapshot_instance._format_value("field", "NaN") is None
        
        # Test normal values remain unchanged
        assert snapshot_instance._format_value("field", 150.0) == 150.0
        assert snapshot_instance._format_value("field", "test") == "test"
        assert snapshot_instance._format_value("field", None) is None


if __name__ == "__main__":
    pytest.main([__file__])
