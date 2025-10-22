# Replace the load_hospital_data function with this:
@st.cache_data
def load_hospital_data():
    try:
        # Use absolute path - replace with your actual path
        absolute_path = "/full/path/to/your/Backend/data/hospitals.csv"
        if os.path.exists(absolute_path):
            df = pd.read_csv(absolute_path)
            st.success(f"✅ Loaded {len(df)} hospitals")
            counties = ["All Counties"] + sorted(df['county'].dropna().unique().tolist())
            return df, counties
        else:
            st.error(f"❌ File not found at: {absolute_path}")
            return None, None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None, None