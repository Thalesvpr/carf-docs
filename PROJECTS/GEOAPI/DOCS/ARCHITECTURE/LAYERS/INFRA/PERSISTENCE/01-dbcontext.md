# DbContext

Configuração do Entity Framework Core DbContext do GEOAPI.

## CARFDbContext

```csharp
public class CARFDbContext : DbContext
{
    private readonly ITenantContext _tenantContext;

    public CARFDbContext(
        DbContextOptions<CARFDbContext> options,
        ITenantContext tenantContext) : base(options)
    {
        _tenantContext = tenantContext;
    }

    public DbSet<Unit> Units => Set<Unit>();
    public DbSet<Holder> Holders => Set<Holder>();
    public DbSet<Community> Communities => Set<Community>();
    public DbSet<Legitimation> Legitimations => Set<Legitimation>();
    public DbSet<UnitHolder> UnitHolders => Set<UnitHolder>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(CARFDbContext).Assembly);
        modelBuilder.HasPostgresExtension("postgis");

        // Global query filter para multi-tenancy
        modelBuilder.Entity<Unit>().HasQueryFilter(u => u.TenantId == _tenantContext.TenantId);
        modelBuilder.Entity<Holder>().HasQueryFilter(h => h.TenantId == _tenantContext.TenantId);
        modelBuilder.Entity<Community>().HasQueryFilter(c => c.TenantId == _tenantContext.TenantId);
    }
}
```

## Configuração de Entidade

```csharp
public class UnitConfiguration : IEntityTypeConfiguration<Unit>
{
    public void Configure(EntityTypeBuilder<Unit> builder)
    {
        builder.ToTable("units");

        builder.HasKey(u => u.Id);
        builder.Property(u => u.Id).HasColumnName("id");

        builder.Property(u => u.Code)
            .HasColumnName("code")
            .HasMaxLength(50)
            .IsRequired();

        builder.HasIndex(u => new { u.TenantId, u.Code }).IsUnique();

        // Geometry com PostGIS
        builder.Property(u => u.Boundary)
            .HasColumnName("boundary")
            .HasColumnType("geometry(Polygon, 4326)");

        builder.Property(u => u.Centroid)
            .HasColumnName("centroid")
            .HasColumnType("geometry(Point, 4326)");

        // Value Objects
        builder.OwnsOne(u => u.Address, addr =>
        {
            addr.Property(a => a.Street).HasColumnName("address_street");
            addr.Property(a => a.Number).HasColumnName("address_number");
            // ...
        });

        // Relacionamentos
        builder.HasMany(u => u.UnitHolders)
            .WithOne(uh => uh.Unit)
            .HasForeignKey(uh => uh.UnitId);

        builder.HasOne(u => u.Community)
            .WithMany(c => c.Units)
            .HasForeignKey(u => u.CommunityId);
    }
}
```

## Registro no DI

```csharp
services.AddDbContext<CARFDbContext>(options =>
{
    options.UseNpgsql(connectionString, npgsql =>
    {
        npgsql.UseNetTopologySuite();
        npgsql.MigrationsAssembly("GEOAPI.Infrastructure");
    });
});
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
