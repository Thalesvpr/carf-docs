-- Function to get current tenant from session variable
CREATE OR REPLACE FUNCTION current_tenant_id()
RETURNS UUID AS $$
BEGIN
  RETURN current_setting('app.tenant_id', true)::uuid;
EXCEPTION
  WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE;

-- Example RLS policy (will be created by EF Core migrations)
-- CREATE POLICY tenant_isolation_policy ON units
--   USING (tenant_id = current_tenant_id());
