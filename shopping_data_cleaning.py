import pandas as pd, numpy as np, kagglehub, csv, os

# load CSV and clean dataset
def load_dataset(filepath):
    df = pd.read_csv(filepath)                             # read dataset
    df.dropna(how='all', inplace=True)                    # remove fully empty rows
    df.replace({"Yes": 1, "No": 0}, inplace=True)         # convert Yes/No to 1/0

    # normalize subscription frequency labels
    df.replace({'Fortnightly': 14, 'Weekly': 7, 'Annually': 360,
                'Quarterly': 90, 'Bi-Weekly': 14, 'Monthly': 30,
                'Every 3 Months': 90}, inplace=True)

    # remove unnamed or blank columns
    unlabeled = [c for c in df.columns 
                 if (c is None) or (isinstance(c, str) and 
                 (c.strip()=='' or c.startswith('Unnamed')))]
    if unlabeled:
        df = df.drop(columns=unlabeled)

    return df                                              # return cleaned dataset


# create age groups based on quartiles
def create_age_groups(df):
    arr = df.Age.quantile([0, 0.25, 0.5, 0.75, 1])         # compute quartiles
    bins = [int(x) for x in arr.values]                    # convert to ints
    labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]  # label bins

    df['Age Range'] = pd.cut(df['Age'], bins=bins,
                             labels=labels, include_lowest=True)  # assign groups


# compute % preferences for size, color, category, etc.
def compute_preferences(df):
    group_cols = ["Age Range", "Gender", "Season",
                  "Subscription Status", "Discount Applied",
                  "Promo Code Used", "Payment Method", "Shipping Type"]  # group fields

    pct = lambda s: (s.value_counts(normalize=True)*100).round(2)        # percentage fn

    size_prefs = df.groupby(group_cols)['Size'].apply(pct).unstack(fill_value=0)      # size %
    color_prefs = df.groupby(group_cols)['Color'].apply(pct).unstack(fill_value=0)    # color %
    category_prefs = df.groupby(group_cols)['Category'].apply(pct).unstack(fill_value=0) # category %

    return size_prefs, color_prefs, category_prefs


# analyze pricing: regional, payment methods, subscriber differences, discounts
def analyze_regional_pricing(df):
    results = {}                                           # store calculations

    # price stats by state
    regional = df.groupby('Location')['Purchase Amount (USD)'] \
                 .agg(mean='mean', median='median', min='min',
                      max='max', std='std', count='count').round(2)
    results['regional_stats'] = regional

    # identify top-selling item
    top_item = df['Item Purchased'].value_counts().idxmax()
    item_df = df[df['Item Purchased'] == top_item]         # filter to most sold item

    # compute avg spend per payment method for that item
    payment_diff = item_df.groupby('Payment Method')['Purchase Amount (USD)'] \
                           .mean().sort_values(ascending=False).round(2)
    results['top_item'] = top_item
    results['payment_method_price_diff'] = payment_diff

    # compute subscriber vs non-subscriber price per state
    state_avg = df.groupby(['Location', 'Subscription Status'])['Purchase Amount (USD)'] \
                  .mean().unstack()
    state_avg.columns = ['Non-Subscriber', 'Subscriber']   # rename cols
    state_avg['Percent Difference'] = ((state_avg['Subscriber'] -
                                        state_avg['Non-Subscriber']) /
                                        state_avg['Non-Subscriber'] * 100).round(2)
    results['subscriber_vs_non'] = state_avg

    # compute discount-only effect
    discount_stats = df.groupby('Discount Applied')['Purchase Amount (USD)'] \
                        .agg(['mean', 'count']).rename(
                        columns={'mean': 'Average Spend',
                                 'count': 'Num Purchases'}).round(2)
    results['discount_effects'] = discount_stats

    # compute promo-only effect
    promo_stats = df.groupby('Promo Code Used')['Purchase Amount (USD)'] \
                     .agg(['mean', 'count']).rename(
                     columns={'mean': 'Average Spend',
                              'count': 'Num Purchases'}).round(2)
    results['promo_effects'] = promo_stats

    results['full_df'] = df                                # keep full df for unified discount analysis
    return results


# generate the final written sales summary
def summarize_findings(size_prefs, color_prefs, category_prefs, results):
    regional = results['regional_stats']                    # regional pricing
    top_item = results['top_item']                          # most purchased item
    payment_diff = results['payment_method_price_diff']     # price by payment method
    subs_table = results['subscriber_vs_non']               # subs vs non-subs
    df = results['full_df']                                 # full dataset

    category_top_items = {}
    for cat in df["Category"].unique():
        most_common_item = df[df["Category"] == cat]["Item Purchased"] \
                            .value_counts().idxmax()
        category_top_items[cat] = f"{cat} ({most_common_item})"

    subs_more = subs_table[subs_table["Percent Difference"] > 0]["Percent Difference"] # subs pay more
    subs_less = subs_table[subs_table["Percent Difference"] < 0]["Percent Difference"] # subs pay less

    # top preferences overall
    # actual top choices across all demographics
    top_size = size_prefs.mean().idxmax()
    top_color = color_prefs.mean().idxmax()
    top_category = category_prefs.mean().idxmax()
    top_category_full = category_top_items[top_category]



    # payment method extremes
    highest_payment_method = payment_diff.idxmax()
    highest_payment_value = payment_diff.max()
    lowest_payment_method = payment_diff.idxmin()
    lowest_payment_value = payment_diff.min()

    # states with highest/lowest spending
    highest_state = regional["mean"].idxmax()
    highest_state_val = regional["mean"].max()
    lowest_state = regional["mean"].idxmin()
    lowest_state_val = regional["mean"].min()

    # unified discount/promo calculation
    df["Any_Discount"] = ((df["Discount Applied"] == 1) |
                          (df["Promo Code Used"] == 1)).astype(int)
    combined = df.groupby("Any_Discount")["Purchase Amount (USD)"].mean().round(2)
    with_any = combined.loc[1] if 1 in combined.index else "N/A"
    without_any = combined.loc[0] if 0 in combined.index else "N/A"

    # build report text
    report = []
    report.append("END-OF-YEAR SALES REPORT")
    report.append("----------------------------------------\n")

    report.append("CUSTOMER PREFERENCES")
    report.append(f"Top Size Preference: {top_size}")
    report.append(f"Top Color Preference: {top_color}")
    report.append(f"Top Category Preference: {top_category_full}\n")
    report.append("\nTOP ITEM PER CATEGORY")
    for cat, txt in category_top_items.items():
        report.append(f"{txt}")
    report.append("\n")
    report.append("PAYMENT METHOD BEHAVIOR")
    report.append(f"Most Popular Item Analyzed: {top_item}")
    report.append(f"Highest Average Spend: {highest_payment_method} (${highest_payment_value})")
    report.append(f"Lowest Average Spend: {lowest_payment_method} (${lowest_payment_value})\n")

    report.append("SUBSCRIBER VS NON-SUBSCRIBER (By State)")
    report.append("States Where Subscribers Pay MORE (%):")
    report.append(subs_more.to_string() if not subs_more.empty else "None")
    report.append("\nStates Where Subscribers Pay LESS (%):")
    report.append(subs_less.to_string() if not subs_less.empty else "None")
    report.append("\n")

    report.append("REGIONAL PRICE SUMMARY")
    report.append(f"Highest-Priced State: {highest_state} (${highest_state_val})")
    report.append(f"Lowest-Priced State: {lowest_state} (${lowest_state_val})\n")

    report.append("DISCOUNT / PROMO EFFECT")
    report.append(f"Average Spend WITH Discount/Promo Applied: ${with_any}")
    report.append(f"Average Spend WITHOUT Discount/Promo: ${without_any}\n")

    return "\n".join(report)                                # return final report text


# write summary to a file
def write_results(summary_text, filename):
    with open(filename, "w", encoding="utf-8") as f:         # write file
        f.write(summary_text)


# ---------------------------------------
# LOAD + PROCESS + ANALYZE + WRITE REPORT
# ---------------------------------------

filepath = "shopping_behavior_updated.csv"                   # dataset path
df = load_dataset(filepath)                                  # load data
create_age_groups(df)                                        # assign age bins

for col in df.columns:                                       # print column values
    print(col)
    print(df[col].unique())

size, color, cat = compute_preferences(df)                   # compute prefs
res = analyze_regional_pricing(df)                           # compute pricing
summary = summarize_findings(size, color, cat, res)          # build report
write_results(summary, "financial_report.txt")               # save report
