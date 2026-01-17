# Background Jobs

Jobs Hangfire para processamento assíncrono.

## Configuração

```csharp
// Program.cs
services.AddHangfire(config =>
{
    config.UsePostgreSqlStorage(connectionString, new PostgreSqlStorageOptions
    {
        QueuePollInterval = TimeSpan.FromSeconds(15)
    });
});

services.AddHangfireServer(options =>
{
    options.Queues = new[] { "critical", "default", "low" };
    options.WorkerCount = Environment.ProcessorCount * 2;
});
```

## Jobs Definidos

### ReportGenerationJob

```csharp
public class ReportGenerationJob
{
    [Queue("default")]
    public async Task GeneratePdfReport(Guid reportId, CancellationToken ct)
    {
        var report = await _reportRepository.GetByIdAsync(reportId, ct);

        // Gerar PDF
        var pdfBytes = await _pdfGenerator.GenerateAsync(report, ct);

        // Upload para storage
        var key = await _storage.UploadAsync(
            new MemoryStream(pdfBytes),
            $"report-{reportId}.pdf",
            "application/pdf", ct);

        // Atualizar status
        report.MarkCompleted(key);
        await _reportRepository.UpdateAsync(report, ct);

        // Notificar usuário
        await _notificationService.NotifyReportReady(report.RequestedBy, reportId, ct);
    }
}
```

### NotificationJob

```csharp
public class NotificationJob
{
    [Queue("critical")]
    public async Task SendEmailNotification(Guid userId, string subject, string body)
    {
        var user = await _userRepository.GetByIdAsync(userId);
        await _emailService.SendAsync(user.Email, subject, body);
    }

    [Queue("low")]
    public async Task SendBulkNotifications(List<Guid> userIds, string subject, string body)
    {
        foreach (var userId in userIds)
        {
            BackgroundJob.Enqueue<NotificationJob>(j =>
                j.SendEmailNotification(userId, subject, body));
        }
    }
}
```

### DataCleanupJob

```csharp
public class DataCleanupJob
{
    [Queue("low")]
    public async Task CleanupExpiredTokens()
    {
        await _tokenRepository.DeleteExpiredAsync();
    }

    [Queue("low")]
    public async Task CleanupTempFiles()
    {
        var expiredFiles = await _storage.ListExpiredTempFilesAsync(TimeSpan.FromDays(1));
        foreach (var file in expiredFiles)
        {
            await _storage.DeleteAsync(file.Key);
        }
    }
}
```

## Recurring Jobs

```csharp
// Program.cs
RecurringJob.AddOrUpdate<DataCleanupJob>(
    "cleanup-expired-tokens",
    j => j.CleanupExpiredTokens(),
    Cron.Daily(3)); // 03:00 UTC

RecurringJob.AddOrUpdate<DataCleanupJob>(
    "cleanup-temp-files",
    j => j.CleanupTempFiles(),
    Cron.Daily(4)); // 04:00 UTC
```

## Enfileirar Jobs

```csharp
// Fire and forget
BackgroundJob.Enqueue<ReportGenerationJob>(j => j.GeneratePdfReport(reportId, default));

// Delayed
BackgroundJob.Schedule<NotificationJob>(
    j => j.SendEmailNotification(userId, "Lembrete", "..."),
    TimeSpan.FromHours(24));
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
