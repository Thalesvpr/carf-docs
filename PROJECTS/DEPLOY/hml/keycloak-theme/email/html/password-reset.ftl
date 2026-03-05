<#import "template.ftl" as layout>
<@layout.emailLayout>
<table style="width: 100%; max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
    <tr>
        <td style="background: #2C5F2D; padding: 20px; text-align: center;">
            <h1 style="color: #FFFFFF; margin: 0;">CARF</h1>
            <p style="color: #97BC62; margin: 5px 0 0 0;">Sistema de Regularização Fundiária</p>
        </td>
    </tr>
    <tr>
        <td style="padding: 30px 20px; background: #FFFFFF;">
            <h2 style="color: #2C5F2D; margin-top: 0;">${msg("passwordResetSubject")}</h2>
            <p style="color: #333333; line-height: 1.6;">
                ${msg("passwordResetBodyHtml", link, realmName, linkExpirationFormatter(linkExpiration))?no_esc}
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="${link}" style="display: inline-block; padding: 12px 30px; background: #2C5F2D; color: #FFFFFF; text-decoration: none; border-radius: 4px; font-weight: bold;">
                    ${msg("passwordResetButton")}
                </a>
            </div>
            <p style="color: #666666; font-size: 14px;">
                ${msg("passwordResetExpiry", linkExpirationFormatter(linkExpiration))}
            </p>
            <p style="color: #D32F2F; font-size: 14px; background: #FFEBEE; padding: 10px; border-left: 3px solid #D32F2F;">
                ${msg("passwordResetWarning")}
            </p>
        </td>
    </tr>
    <tr>
        <td style="background: #F5F5F5; padding: 20px; text-align: center; font-size: 12px; color: #666666;">
            <p style="margin: 5px 0;">Sistema CARF - Lei 13.465/2017</p>
            <p style="margin: 5px 0;">${msg("emailFooter")}</p>
        </td>
    </tr>
</table>
</@layout.emailLayout>
