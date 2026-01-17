# File Storage

Implementação de armazenamento de arquivos com S3-compatible storage.

## IFileStorage

```csharp
public interface IFileStorage
{
    Task<string> UploadAsync(Stream stream, string fileName, string contentType, CancellationToken ct = default);
    Task<Stream> DownloadAsync(string key, CancellationToken ct = default);
    Task DeleteAsync(string key, CancellationToken ct = default);
    Task<string> GetPresignedUrlAsync(string key, TimeSpan expiration, CancellationToken ct = default);
}
```

## S3FileStorage

```csharp
public class S3FileStorage : IFileStorage
{
    private readonly IAmazonS3 _s3Client;
    private readonly ITenantContext _tenantContext;
    private readonly string _bucketName;

    public async Task<string> UploadAsync(Stream stream, string fileName, string contentType, CancellationToken ct)
    {
        var key = GenerateKey(fileName);

        var request = new PutObjectRequest
        {
            BucketName = _bucketName,
            Key = key,
            InputStream = stream,
            ContentType = contentType,
            Metadata =
            {
                ["tenant-id"] = _tenantContext.TenantId.ToString()
            }
        };

        await _s3Client.PutObjectAsync(request, ct);
        return key;
    }

    public async Task<string> GetPresignedUrlAsync(string key, TimeSpan expiration, CancellationToken ct)
    {
        var request = new GetPreSignedUrlRequest
        {
            BucketName = _bucketName,
            Key = key,
            Expires = DateTime.UtcNow.Add(expiration)
        };

        return _s3Client.GetPreSignedURL(request);
    }

    private string GenerateKey(string fileName)
    {
        var extension = Path.GetExtension(fileName);
        return $"{_tenantContext.TenantId}/{DateTime.UtcNow:yyyy/MM}/{Guid.NewGuid()}{extension}";
    }
}
```

## Configuração

```csharp
// appsettings.json
{
  "Storage": {
    "Provider": "S3",  // ou "MinIO" para dev
    "BucketName": "carf-documents",
    "Region": "sa-east-1",
    "Endpoint": "https://s3.sa-east-1.amazonaws.com"  // MinIO: "http://localhost:9000"
  }
}

// Program.cs
services.AddSingleton<IAmazonS3>(sp =>
{
    var config = new AmazonS3Config
    {
        ServiceURL = storageOptions.Endpoint,
        ForcePathStyle = storageOptions.Provider == "MinIO"
    };
    return new AmazonS3Client(config);
});
```

## Upload de Fotos

```csharp
public class PhotoService
{
    public async Task<PhotoDto> UploadPhotoAsync(IFormFile file, Guid unitId, CancellationToken ct)
    {
        // Validar tipo e tamanho
        if (!AllowedTypes.Contains(file.ContentType))
            throw new ValidationException("Tipo de arquivo não permitido");

        if (file.Length > MaxSizeBytes)
            throw new ValidationException("Arquivo muito grande");

        // Gerar thumbnail
        using var thumbnail = await _imageProcessor.CreateThumbnailAsync(file.OpenReadStream());

        // Upload original e thumbnail
        var originalKey = await _storage.UploadAsync(file.OpenReadStream(), file.FileName, file.ContentType, ct);
        var thumbnailKey = await _storage.UploadAsync(thumbnail, $"thumb_{file.FileName}", "image/jpeg", ct);

        return new PhotoDto(originalKey, thumbnailKey);
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
