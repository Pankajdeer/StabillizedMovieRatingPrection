
#pca on normalised data
data_reduc_pca=data2_movies[['Budget','percent_collected', 'Genre_no', 'Runtime', 'Director_Oscar', 'Director_Wins', 'Writer_Oscar', 'Writer_Wins','Actor_Oscar', 'Actor_Wins', 'perc_positive', 'perc_negative', 'perc_neutral']]
column_names= data_reduc_pca.columns

data_reduc_pca_values = data_reduc_pca.values


#performing PCA on normalized data
scaler = preprocessing.MinMaxScaler()
data_reduc_pca_scaled = scaler.fit_transform(data_reduc_pca_values)
data_reduc_pca_norm = pd.DataFrame(data_reduc_pca_scaled,columns = column_names)
data_reduc_pca_norm

#
pca_result = pca(n_components=13).fit(data_reduc_pca)

#Obtain eigenvalues
print(pca_result.explained_variance_)

#Components from the PCA
print(pca_result.components_.T * np.sqrt(pca_result.explained_variance_))

#screeplot
# Run this group of code together by highlighting it
# all and then running it

plt.figure(figsize=(7,5))
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13], pca_result.explained_variance_ratio_, '-o')
plt.ylabel('Proportion of Variance Explained') 
plt.xlabel('Principal Component') 
plt.xlim(0.75,4.25) 
plt.ylim(0,1.05) 
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13])
